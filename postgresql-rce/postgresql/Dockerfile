# syntax=docker/dockerfile:1

FROM postgres
ENV POSTGRES_USER docker
ENV POSTGRES_PASSWORD sososecret
ENV POSTGRES_DB docker


RUN apt update && \
 DEBIAN_FRONTEND=noninteractive \
 apt-get install -y --allow-downgrades --allow-remove-essential --allow-change-held-packages \
 python3-pip \
 libpq-dev

ADD ../ /app
WORKDIR /app/

EXPOSE 5432

CMD ["postgres"]
