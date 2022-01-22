# syntax=docker/dockerfile:1

FROM ubuntu:20.04
RUN apt update && \
 DEBIAN_FRONTEND=noninteractive \
 apt-get install -y --allow-downgrades --allow-remove-essential --allow-change-held-packages \
 openjdk-8-jre-headless \
 python3-pip \
 wget \
 screen

ADD . /app
WORKDIR /app/

RUN wget https://papermc.io/api/v2/projects/paper/versions/1.16.5/builds/700/downloads/paper-1.16.5-700.jar

EXPOSE 8123
EXPOSE 25565

CMD ["screen", "-m", "./start.sh"]
# java -Xms2G -Xmx2G -jar paper-1.16.5-700.jar --nogui