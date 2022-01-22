# syntax=docker/dockerfile:1

FROM python:latest
RUN apt update && \
 DEBIAN_FRONTEND=noninteractive \
 apt-get install -y --allow-downgrades --allow-remove-essential --allow-change-held-packages \
 python3-pip

ADD . /app
WORKDIR /app/

EXPOSE 8001

RUN python3 -m pip install -r requirements.txt
CMD python3 manage.py
