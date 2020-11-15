FROM ubuntu:18.04
MAINTAINER Timofey Durakov (timofei.nd@gmail.com)

ENV PACKAGE kafka_2.12-2.3.0

WORKDIR /tmp/

RUN  apt-get update \
  && apt-get install -y wget \
  && apt-get install -y openjdk-8-jdk

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
RUN export JAVA_HOME

RUN    wget -q https://archive.apache.org/dist/kafka/2.3.0/$PACKAGE.tgz \
    && wget -q https://archive.apache.org/dist/kafka/2.3.0/$PACKAGE.tgz.md5 \
    && sed 's/\ //g' $PACKAGE.tgz.md5 > $PACKAGE.tmp.md5 \
    && awk -F ":" '{print $2 " " $1}' $PACKAGE.tmp.md5 > $PACKAGE.tgz.md5 \
    && md5sum -c $PACKAGE.tgz.md5 \
    && tar -xzf $PACKAGE.tgz --directory /opt/ \
    && ln -s /opt/$PACKAGE /opt/kafka \
    && rm -rfv /tmp/*

COPY server.properties /opt/kafka/config/server.properties

WORKDIR /opt/kafka/
