#!/usr/bin/env python3

import logging
import ssl
from ibmiotf.application import Client
import click
import paho.mqtt.client as mqtt


def with_paho(host, port, user, pw, pub, sub, client_id, transport):
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        print("Subscribing to {}".format(sub))
        client.subscribe(sub)

        if pub:
            client.publish(
                pub,
                "Hello",
            )

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))

    client = mqtt.Client(client_id=client_id, transport=transport)
    client.on_connect = on_connect
    client.on_message = on_message

    client.username_pw_set(user, pw)
    client.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2)

    print(host)

    print(client.connect(host, port, 60))

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_forever()


def with_ibm(host, port, user, pw, pub, sub, client_id, transport):
    options = {
        "org": "abc123",
        "broker-url": host,
        "port": port,
        "auth-key": user,
        "auth-token": pw,
        "full_client_id": client_id,
        "use-websockets": transport == "websockets",
        "tls-version": "PROTOCOL_TLSv1_2",
    }

    Client(options).connect()


@click.command()
@click.option("--lib")
@click.option("--host", default="localhost")
@click.option("--port", default=8080)
@click.option("--user", default="v1:CoolProject:aircon:0xbeef")
@click.option("--pw", default="p:fada60ac-f686-46db-9234-1a140753c932")
@click.option("--sub", default="/iot-2/type/gateway/id/v1:pid123:aircon:0xbeef/cmd/boom/fmt/json")
@click.option("--pub", default="/iot-2/type/gateway/id/v1:pid123:aircon:0xbeef/evt/boom/fmt/json")
@click.option("--transport", default="websockets")
@click.option("--client_id", default="overlocktestclient")
def run(lib, host, port, user, pw, pub, sub, client_id, transport):
    logging.basicConfig(level=logging.DEBUG)

    if lib == "paho":
        with_paho(host, port, user, pw, pub, sub, client_id, transport)
    else:
        with_ibm(host, port, user, pw, pub, sub, client_id, transport)


if __name__ == "__main__":
    run()
