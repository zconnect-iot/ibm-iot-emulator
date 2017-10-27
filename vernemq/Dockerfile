FROM erlio/docker-vernemq as builder

# Nothing - just use this as a base

#MAINTAINER Erlio GmbH info@vernemq.com
#
#RUN apt-get update \
#    && apt-get install -y --no-install-recommends \
#    libssl-dev \
#    logrotate \
#    sudo \
#    wget \
#    && rm -rf /var/lib/apt/lists/*
#
#ENV VERNEMQ_VERSION 1.0.0rc2
#
#ADD vernemq_$VERNEMQ_VERSION-1_amd64.deb /tmp/vernemq.deb
#
#RUN dpkg -i /tmp/vernemq.deb
#
#ADD files/config/vernemq.conf /etc/vernemq/vernemq.conf
#ADD files/config/vm.args /etc/vernemq/vm.args
#ADD bin/vernemq.sh /usr/sbin/start_vernemq
#ADD bin/rand_cluster_node.escript /var/lib/vernemq/rand_cluster_node.escript


FROM alpine:latest

COPY --from=builder /usr/sbin/vmq-admin     /usr/sbin/vmq-admin
COPY --from=builder /usr/sbin/vmq-passwd    /usr/sbin/vmq-passwd
COPY --from=builder /usr/sbin/vernemq       /usr/sbin/vernemq
#COPY --from=builder /usr/sbin/start_vernemq /usr/sbin/start_vernemq

COPY --from=builder /usr/lib/vernemq/lib/ /usr/lib/vernemq/lib/
COPY --from=builder /usr/lib/vernemq/releases/ /usr/lib/vernemq/releases/
COPY --from=builder /usr/lib/vernemq/erts-8.2/ /usr/lib/vernemq/erts-8.2/
COPY --from=builder /etc/vernemq/ /etc/vernemq/

RUN apk update \
    && apk add --no-cache --virtual .fetch-deps \
        grep bash openssl logrotate \
    && rm -rf /var/cache/apk/*

ADD bin/vernemq.sh /usr/sbin/start_vernemq

# MQTT
EXPOSE 1883 

# MQTT/SSL
EXPOSE 8883

# MQTT WebSockets
EXPOSE 8080

# VerneMQ Message Distribution
#EXPOSE 44053

# EPMD - Erlang Port Mapper Daemon
#EXPOSE 4369
    
# Specific Distributed Erlang Port Range 
#EXPOSE 9100 9101 9102 9103 9104 9105 9106 9107 9108 9109

# Prometheus Metrics
#EXPOSE 8888

VOLUME ["/var/log/vernemq", "/var/lib/vernemq", "/etc/vernemq"]

RUN addgroup -S vernemq
RUN adduser -S -D -g '' vernemq -G vernemq

CMD ["start_vernemq"] 
