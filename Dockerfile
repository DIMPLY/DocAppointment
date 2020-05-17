#
# modified from example Dockerfile for https://docs.docker.com/engine/examples/postgresql_service/
#
FROM ubuntu:16.04
MAINTAINER Yan Yang "yy4jobs@gmail.com"

# Install ``python-software-properties``, ``software-properties-common`` and PostgreSQL 9.3
#  There are some warnings (in red) that show up during the build. You can hide
#  them by prefixing each apt-get statement with DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y python-software-properties software-properties-common python3-pip python3-dev && pip3 install --upgrade pip

EXPOSE 5002

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

# Note: The official Debian and Ubuntu images automatically ``apt-get clean``
# after each ``apt-get``

# Expose the DocApp port
VOLUME ["./logs"]
# Set the default command to run when starting the container
CMD python3 docapp.py >> logs/backend.log

