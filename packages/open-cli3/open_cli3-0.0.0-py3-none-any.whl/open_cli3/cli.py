#!/usr/bin/python3
"""Open-CLI."""
import os
import configparser
import logging
import warnings
import requests
import yaml

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from pyfiglet import print_figlet

from . import help
from . import parser
from . import completer
from . import formatter
from .openapi_extension import OpenAPIExt

# Suppress bravado warnings
warnings.filterwarnings("ignore")

DEFAULT_SECTION = "DEFAULT"
CONFIG_OPTIONS = {0: "endpoint", 1: "access_token"}


class OpenCLI:
    """CLI processor."""

    def __init__(
        self, source, history_path, profile_name, print_request_time=False, output_format=formatter.JSON, headers=None
    ):
        """Initialize the CLI processor."""
        self.history_path = history_path
        self.output_format = output_format
        self.print_request_time = print_request_time
        self.profile_name = profile_name
        self.config_file_path = os.path.join(os.path.expanduser("~"), ".open-cli3-config/config.cfg")

        self.logger = logging.getLogger("open-cli3")
        self.logger.debug(
            "Creating a python client based on %s, headers: %s", source, headers
        )

        headers = self._parse_headers(headers)

        # parse profile_name and/or source attributes
        endpoint_opt = CONFIG_OPTIONS[0]
        if profile_name:
            config_obj = self._get_config_object(self.config_file_path)
            endpoint = ""
            if config_obj:
                endpoint = self._get_option_from_config_obj(config_obj, endpoint_opt)
            else:
                self.logger.debug("You don't have open-cli3 config file, so we will use source attribute instead")
                config_obj = configparser.ConfigParser()
            if source:
                endpoint = source
            else:
                self.logger.debug("You don't have open-cli3 config file for profile name and you additionally "
                                    "didn't provide source attribute instead")
            section = self.profile_name if self.profile_name else DEFAULT_SECTION
            if section != DEFAULT_SECTION and not config_obj.has_section(section):
                config_obj.add_section(section)
            config_obj.set(section, endpoint_opt, endpoint)
            os.makedirs(os.path.dirname(self.config_file_path), exist_ok=True)
            with open(self.config_file_path, 'w') as configfile:
                config_obj.write(configfile)

        elif source:
            endpoint = source
        else:
            raise Exception("You should specify at least source or profile name (if exists) "
                            "in order to run open-cli3. Check 'help' (-h, --help) for more information")

        # Handle non-url sources
        spec = None
        if os.path.exists(endpoint):
            with open(endpoint) as f:
                spec = yaml.safe_load(f.read())

        if not spec:
            spec = requests.get(endpoint).json()
        self.client = OpenAPIExt(spec)

        # Get the CLI prompt name from the spec title
        self.name = self.client.info.title

        # Initialize a command parser based on the client
        self.command_parser = parser.CommandParser(client=self.client)

    def run_loop(self):
        """Run the CLI loop."""
        history = FileHistory(self.history_path)
        command_completer = completer.CommandCompleter(client=self.client)
        print_figlet("PrivCloud", font="starwars", width=100)

        while True:

            try:
                input_text = prompt(
                    u"%s $ " % self.name,
                    history=history,
                    completer=command_completer,
                    auto_suggest=AutoSuggestFromHistory(),
                )
                self.execute(command=input_text)

            except KeyboardInterrupt:
                exit("User Exited")

            except Exception as exc:
                self.logger.error(exc)

    def execute(self, command):
        """Parse and execute the given command."""
        self.logger.debug("Invoke authentication")
        token_opt = CONFIG_OPTIONS[1]
        config_obj = self._get_config_object(self.config_file_path)
        if config_obj:
            access_token = self._get_option_from_config_obj(config_obj, token_opt)
            if access_token:
                for k in self.client.components.securitySchemes.keys():
                    self.client.authenticate(k, access_token)
            else:
                self.logger.debug(f"You don't have access token for such profile name <{self.profile_name}> or "
                                  f"for 'DEFAULT' section in your open-cli3 config file")
        else:
            self.logger.debug("You don't have open-cli3 config file")

        self.logger.debug("Parsing the input text %s", command)
        operation, arguments = self.command_parser.parse(text=command)

        if help.is_requested(arguments):
            self.logger.debug("Help requested for operation %s", operation)
            return help.show(operation)

        self.logger.debug("Invoke operation %s with arguments %s", operation, arguments)
        response = operation(**arguments)

        if not isinstance(response, list):
            if hasattr(response, "_raw_data"):
                access_token = response._raw_data.get("access_token")
                expires_at = response._raw_data.get("expires_at")
                if access_token and expires_at:
                    section = self.profile_name if self.profile_name else DEFAULT_SECTION
                    if not config_obj:
                        config_obj = configparser.ConfigParser()
                        if section != DEFAULT_SECTION:
                            config_obj.add_section(section)
                    config_obj.set(section, token_opt, access_token)
                    os.makedirs(os.path.dirname(self.config_file_path), exist_ok=True)
                    with open(self.config_file_path, 'w') as configfile:
                        config_obj.write(configfile)

        if isinstance(response, list):
            response = [r._raw_data for r in response]
        else:
            if hasattr(response, "_raw_data"):
                response = response._raw_data
        self.logger.debug("Formatting response %s", response)
        print(formatter.format_response(response, output_format=self.output_format))
        if self.print_request_time:
            print(f"Request time: {self.client.request_time_sec} seconds")

    @staticmethod
    def _parse_headers(headers):
        """Parse headers list into a dictionary."""
        try:
            return dict(header.split(":") for header in headers)
        except:
            raise ValueError("Invalid headers %s" % headers)

    @staticmethod
    def _get_config_object(conf_file_path):
        config_obj = None
        if os.path.exists(conf_file_path):
            config = configparser.ConfigParser()
            config.read_file(open(conf_file_path))
            config_obj = config
        return config_obj

    def _get_option_from_config_obj(self, config_obj, option):
        option_val = ""
        if config_obj.has_section(self.profile_name) and config_obj.has_option(self.profile_name, option):
            option_val = config_obj.get(self.profile_name, option)
        else:
            self.logger.debug(f"You don't have such profile name <{self.profile_name}> "
                              f"in your open-cli3 config file. We wil try to use data from <{DEFAULT_SECTION}> "
                              f"section of your open-cli3 config file")
            if config_obj.defaults() and config_obj.has_option(DEFAULT_SECTION, option):
                option_val = config_obj.get(DEFAULT_SECTION, option)
            else:
                self.logger.debug(f"Neither <{self.profile_name}> nor <{DEFAULT_SECTION}> sections are located "
                                  f"in your open-cli3 config file")
        return option_val
