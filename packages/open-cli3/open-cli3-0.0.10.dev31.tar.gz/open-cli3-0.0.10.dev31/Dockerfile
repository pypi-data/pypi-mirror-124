FROM python:3.6 AS build

# Set build work directory
WORKDIR /open-cli3/

# Install build requirements
RUN pip install pbr==1.8.0

# Copy config files into the build container
COPY .git /open-cli3/.git
COPY LICENSE /open-cli3/LICENSE
COPY setup.py /open-cli3/setup.py
COPY setup.cfg /open-cli3/setup.cfg
COPY README.md /open-cli3/README.md
COPY requirements.txt /open-cli3/requirements.txt

# Copy package code into the build container
COPY open_cli3/*.py /open-cli3/open_cli3/

# Build the package and set its name
RUN python setup.py sdist && mv dist/open-cli*.tar.gz dist/open-cli3.tar.gz

# -----------------------------------------------------------------------

FROM python:3.6-alpine AS release

# Set entrypoint
ENTRYPOINT ["open-cli3"]

# Copy & install package requirements
ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Copy & install packge
COPY --from=build /open-cli3/dist/open-cli3.tar.gz /open-cli3.tar.gz
RUN pip install --no-cache --no-deps /open-cli3.tar.gz
