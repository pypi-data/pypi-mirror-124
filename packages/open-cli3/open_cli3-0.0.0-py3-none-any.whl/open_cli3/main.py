import os
import logging
import argparse
from distutils.util import strtobool

from . import cli
from . import formatter

HISTORY_PATH = os.path.join(os.path.expanduser("~"), ".open-cli3")


def main():
    """Open-CLI entry point."""
    args_parser = argparse.ArgumentParser(description="Open-CLI.")
    args_parser.add_argument("-s", "--source", type=str, default=None, help="Open API spec source")
    args_parser.add_argument(
        "-v", "--verbose", action="store_true", help="If set, set log level to debug"
    )
    args_parser.add_argument(
        "-t", "--history", type=str, default=HISTORY_PATH, help="History file path"
    )
    args_parser.add_argument(
        "-c", "--command", type=str, help="Command (request) to execute", nargs='+', required=False
    )
    args_parser.add_argument(
        "-f",
        "--format",
        type=str,
        choices=formatter.FORMATTERS.keys(),
        default=formatter.JSON,
        help="Set the CLI output format",
    )
    args_parser.add_argument(
        "--header",
        nargs="+",
        default=[],
        help="Requests headers, usage: --header x-header-1:val-1 x-header-2:val2",
    )
    args_parser.add_argument(
        "--print-request-time",
        type=strtobool,
        default=False,
        help="Show time of each request if this flag set to true",
    )
    args_parser.add_argument(
        "--profile",
        type=str,
        default=None,
        help="Open API profile name that point out some settings you can apply to a open-cli3 command and "
             "which are located in open-cli3 config file")

    args = args_parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.ERROR)

    open_cli = cli.OpenCLI(
        source=args.source,
        history_path=args.history,
        output_format=args.format,
        headers=args.header,
        print_request_time=args.print_request_time,
        profile_name=args.profile,
    )

    if args.command:
        return open_cli.execute(command=args.command[0])

    open_cli.run_loop()


if __name__ == "__main__":
    main()
