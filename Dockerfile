FROM ubuntu:16.04

MAINTAINER Yan Yang "yy4jobs@gmail.com"

RUN apt-get update -y && apt-get install -y python3-pip python3-dev && pip install --upgrade pip

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "docapp.py" ]
