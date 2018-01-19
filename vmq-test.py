import click
import paho.mqtt.client as mqtt


@click.command()
@click.option("--host", default="localhost")
@click.option("--port", default=8080)
@click.option("--user", default="v1:CoolProject:aircon:0xbeef")
@click.option("--pw", default="p:fada60ac-f686-46db-9234-1a140753c932")
@click.option("--sub", default="/iot-2/type/gateway/id/v1:pid123:aircon:0xbeef/cmd/boom/fmt/json")
@click.option("--pub", default="/iot-2/type/gateway/id/v1:pid123:aircon:0xbeef/evt/boom/fmt/json")
@click.option("--client_id", default="overlocktestclient")
def run(host, port, user, pw, pub, sub, client_id):
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

    client = mqtt.Client(client_id=client_id, transport="websockets")
    client.on_connect = on_connect
    client.on_message = on_message

    client.username_pw_set(user, pw)

    print(host)

    print(client.connect(host, port, 60))

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_forever()


if __name__ == "__main__":
    run()
