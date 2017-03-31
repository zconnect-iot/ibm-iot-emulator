FROM debian:jessie

MAINTAINER Erlio GmbH info@vernemq.com

RUN apt-get update && apt-get install -y \
    libssl-dev \
    logrotate \
    sudo \
&& rm -rf /var/lib/apt/lists/*

ENV VERNEMQ_VERSION 1.0.0rc2

ADD https://bintray.com/artifact/download/erlio/vernemq/deb/jessie/vernemq_$VERNEMQ_VERSION-1_amd64.deb /tmp/vernemq.deb

RUN dpkg -i /tmp/vernemq.deb
RUN rm /tmp/vernemq.deb

ADD files/config/vm.args /etc/vernemq/vm.args
ADD files/config/vernemq.conf /etc/vernemq/vernemq.conf
ADD bin/vernemq.sh /usr/sbin/start_vernemq
ADD bin/rand_cluster_node.escript /var/lib/vernemq/rand_cluster_node.escript


# MQTT
EXPOSE 1883 

# MQTT/SSL
EXPOSE 8883

# MQTT WebSockets
EXPOSE 8080

# VerneMQ Message Distribution
EXPOSE 44053

# EPMD - Erlang Port Mapper Daemon
EXPOSE 4369
    
# Specific Distributed Erlang Port Range 
EXPOSE 9100 9101 9102 9103 9104 9105 9106 9107 9108 9109

# Prometheus Metrics
EXPOSE 8888

VOLUME ["/var/log/vernemq", "/var/lib/vernemq", "/home/bitdivision/iot/ibm-iot-emulator/vernemq/files/config:/etc/vernemq"]

CMD ["start_vernemq"] 
