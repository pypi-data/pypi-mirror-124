# Open-CLI3
![Build Status](https://codebuild.us-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiR2ZJNFp4S243bmNBVW13VGRuQkNndGRuVVRiK2tzSDhGRkcyQ1BhRWdCZXlnaGI0T2E5MlJ0dElzbjFqNEY5ZHFZcDdKYS9JT0h1SmVLdjF3Q1RDUnVZPSIsIml2UGFyYW1ldGVyU3BlYyI6Im9sdXhWQnh5K2FoMWI5NnYiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)

A CLI for every service which exposes a OpenAPI (Swagger) specification endpoint.

From the OpenAPI Specification project:

> The goal of The OpenAPI Specification is to define a standard, language-agnostic interface to REST APIs which allows both humans and computers to discover and understand the capabilities of the service without access to source code, documentation, or through network traffic inspection.

## Demo

![Alt Text](https://github.com/privcloud-com/open-cli/blob/master/demo.gif)
![Alt Text](https://github.com/privcloud-com/open-cli/blob/master/demo_table.gif)
![Alt Text](https://github.com/privcloud-com/open-cli/blob/master/demo_profile.gif)

## Docker

To start a CLI session run:

    docker run -it privcloudcom/open-cli3 -s <swagger-spec-url>

e.g:

    docker run -it privcloudcom/open-cli3 -s http://petstore.swagger.io/v3/swagger.json


## CLI session

To start a CLI session run:

    open-cli3 -s <swagger-spec-url>

e.g:

    open-cli3 -s https://raw.githubusercontent.com/OAI/OpenAPI-Specification/main/examples/v3.0/petstore-expanded.json

Running CLI session will automatically create config file at path ```~/.open-cli3-config/config.cfg```

To use profile config pass profile flag with desired profile name:

    open-cli3 --profile <profile_name>

e.g.:

    open-cli3 --profile profile1

This will work only if you specify profile in your open-cli3 config file: path ```~/.open-cli3-config/config.cfg```.
Example of config file: 

```config.cfg

[profile1]
endpoint = <endpoint>
access_token = <access_token>

``` 

To get data without running CLI session, please specify ```-c``` flag. It will automatically execute specified command
and return result data. Example: 
    
    open-cli3 -s <swagger-spec-url> -c 'auth:login --body.email=<user_email> --body.password=<user_password>'

or 
    
    open-cli3 --profile profile1 -c 'auth:login --body.email=<user_email> --body.password=<user_password>'

). 

If a profile name (```--profile``` flag) and swagger url (```-s``` flag) are provided (example: 
    
    open-cli3 -s <swagger-spec-url> --profile profile1
    
), the profile will take precedence. If such profile does not exist CLI will automatically create config file for the 
profile.

If you want to measure the request and response total time you should use ```--print-request-time``` flag. Example:

    open-cli3 -s <swagger-spec-url> --print-request-time true
   
For help run:

    open-cli3 -h

Credits
-------
This project relies on OpenApi3 [openapi3](https://github.com/Dorthu/openapi3) project & on Jonathan Slenders [python-prompt-toolkit](https://github.com/jonathanslenders/python-prompt-toolkit).
