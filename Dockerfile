#
# modified from example Dockerfile for https://docs.docker.com/engine/examples/postgresql_service/
#
FROM ubuntu:16.04
MAINTAINER Yan Yang "yy4jobs@gmail.com"

WORKDIR /app

COPY . /app

# Install ``python-software-properties``, ``software-properties-common`` and PostgreSQL 9.3
#  There are some warnings (in red) that show up during the build. You can hide
#  them by prefixing each apt-get statement with DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y curl dnsutils wget python-software-properties software-properties-common python3-pip python3-dev && pip3 install --upgrade pip && pip3 install -r requirements.txt && su - && apt-get install sudo -y

# Note: The official Debian and Ubuntu images automatically ``apt-get clean``
# after each ``apt-get``

# Expose the DocApp port
EXPOSE 5002

# Set the default command to run when starting the container
CMD ['python3', 'docapp.py']

