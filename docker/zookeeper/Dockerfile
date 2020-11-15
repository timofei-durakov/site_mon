FROM ubuntu:18.04
MAINTAINER Timofey Durakov (timofei.nd@gmail.com)

ENV PACKAGE apache-zookeeper-3.5.6-bin

WORKDIR /tmp/

RUN  apt-get update \
  && apt-get install -y wget \
  && apt-get install -y openjdk-8-jdk

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
RUN export JAVA_HOME

RUN    wget -q https://archive.apache.org/dist/zookeeper/zookeeper-3.5.6/$PACKAGE.tar.gz \
    && wget -q https://archive.apache.org/dist/zookeeper/zookeeper-3.5.6/$PACKAGE.tar.gz.sha512 \
    && sha512sum -c $PACKAGE.tar.gz.sha512 \
    && tar -xzf $PACKAGE.tar.gz --directory /opt/ \
    && ln -s /opt/$PACKAGE /opt/zookeeper \
    && rm -rfv /tmp/*
RUN mv /opt/zookeeper/conf/zoo_sample.cfg /opt/zookeeper/conf/zoo.cfg
WORKDIR /opt/zookeeper/