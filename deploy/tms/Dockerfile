# syntax=docker/dockerfile:1

FROM debian

USER root

WORKDIR /app

RUN apt-get update

RUN apt-get install -y python3-pip python3-venv python3-dev libpq-dev git

COPY . .

RUN pip install -r requirements.txt --break-system-packages

RUN chmod 777 /app/deploy/tms/start.sh

EXPOSE 8000