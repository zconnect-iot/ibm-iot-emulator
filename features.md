- An MQTT broker which behaves in the same way as IBM IoT including QoS and republishing.
- Host a REST API which emulates the IBM IoT API.
- Keep detailed logs of requests / messages to aid in debugging.
- Switcheable authentication proxy to IBM. Either predefined credentials or proxy to IBM.
- Hosted in a docker container to give high portability.
- Simple python interface to the broker which allows asserting that messages are received / sent.
- Allow injection of errors: Broker Not Responding / Authentication errors / etc.
- Ability to throttle broker throughput.
- Application throughput testing.