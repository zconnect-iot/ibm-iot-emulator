FROM erlio/docker-vernemq as builder

# Nothing - just use this as a base


FROM debian:jessie-slim

COPY --from=builder /usr/sbin/vmq-admin     /usr/sbin/vmq-admin
COPY --from=builder /usr/sbin/vmq-passwd    /usr/sbin/vmq-passwd
COPY --from=builder /usr/sbin/vernemq       /usr/sbin/vernemq
COPY --from=builder /usr/share/             /usr/share/
COPY --from=builder /var/lib/vernemq        /var/lib/vernemq
COPY --from=builder /etc/vernemq/ /etc/vernemq/

#COPY --from=builder /usr/lib/vernemq/ /usr/lib/vernemq/
COPY --from=builder /usr/lib/vernemq/lib/ /usr/lib/vernemq/lib/
COPY --from=builder /usr/lib/vernemq/releases/ /usr/lib/vernemq/releases/
COPY --from=builder /usr/lib/vernemq/erts-8.2/bin/ /usr/lib/vernemq/erts-8.2/bin/
COPY --from=builder /usr/lib/vernemq/erts-8.2/lib/ /usr/lib/vernemq/erts-8.2/lib/

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
EXPOSE 8888

VOLUME ["/var/log/vernemq", "/var/lib/vernemq", "/etc/vernemq"]

RUN addgroup --system vernemq
RUN adduser --system --disabled-password --gecos '' --ingroup vernemq vernemq

COPY --from=builder /usr/sbin/start_vernemq /usr/sbin/start_vernemq

CMD ["start_vernemq"]
