IBM IoT Local Broker
===================

Objective
--------
Create an equivalent to the IBM IoT platform which can be easily set up and run locally and will work with existing IBM provided libraries.

Why
---
Currently, to perform end-to-end tests with IBM without polluting production data, users must create new IBM accounts. These need to be changed whenever the free trial expires.

It would be useful to have a sandbox system which could be brought up when performing tests. Additionally, being able to view logs etc would make debugging simpler.

What
--------
- Host an MQTT broker which acts in the same way as the IBM MQTT broker
    - Republishing topics
    - Authentication
    - Status Messages
- Host an API which emulates the IBM IoT API
- Show detailed logs of requests / messages to aid in debugging
- Switcheable authentication proxy to IBM. Either predefined credentials or proxy to IBM
- Hosted in a docker container to give high portability.

### Optional Features
- Add a simple python interface to the broker which allows asserting that messages are received / sent
- Allow injection of errors broker not responding / Authentication errors / etc.
- Allow throttling
- Throughput testing

How
---

### Stage 1
- Docker container runs everything. Configuration file accessed through docker volume with sane defaults.
- Preset username / password for authentication from settings file
- Python application subscribed to `#` which will perform republishing

#### Broker
Mosquitto is the obvious choice however it's plugin architecture is poor. Mosquitto doesn't really provide hooks for things like disconnection / connection which are needed to emulate IBM.

Other Broker Options:
    - VerneMQ - Apache2 License, plugins have to be written in Erlang.
    - HiveMQ - Closed
    - emqttd - Plugins must be written in Erlang.
    - Apache ActiveMQ - Java plugins, very enterprise.

QoS 0, 1, 2 are supported by all of the above brokers.

It would be possible to hack mosquitto to support connection / disconnection events using the auth plugin for connection and LWT for disconnection but the plugin system is going to cause issues when developing features like access control for gateways which require hooks into the core publish / subscribe functionality.

Ignoring ActiveMQ for the moment, the options are either VerneMQ or emqttd. emqttd doesn't seem to be hugely well documented whereas VerneMQ has great documentation, a very flexible plugin system, and the possibility to write basic plugins in Lua.

The main feature of the plugin at this stage will be to publish connection and disconnection events on a @sys type topic so that the python application can pick up any events. This removes the need for any kind of RPC system between erlang / lua and python.

Later, the broker plugin will need to be extended to support access control. This would require a database of some kind and would need to intercept all subscriptions / publish events to ensure resource groups match.

#### Republishing

Currently IBM appears to perform the following on top of the basic MQTT protocol.

Publish Connect / Disconnect messages on `iot-2/type/+/id/+/mon` and Application status messages on `iot-2/app/+/mon`

The VernMQ plugin would need to hook into `on_register` and `on_client_offline` / `on_client_gone`

Stage 2
- Basic API for management of devices / authentication 


