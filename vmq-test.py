import click
import paho.mqtt.client as mqtt


@click.command()
@click.option("--host", required=True)
@click.option("--port", default=80)
@click.option("--user", default="use-token-auth")
@click.option("--pw", default="-ankVuPqceD(LBd0Zc")
@click.option("--sub", default="$SYS/#")
@click.option("--client_id", default="g:veejb5:novo-gateway:576127cb94149d536f8e6a93")
def run(host, port, user, pw, sub, client_id):
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        print("Subscribing to {}".format(sub))
        client.subscribe(sub)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))

    client = mqtt.Client(client_id=client_id, transport="websockets")
    client.on_connect = on_connect
    client.on_message = on_message

    client.username_pw_set("use-token-auth", pw)

    print(host)

    print(client.connect(host, port, 60))

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    # client.loop_forever()


if __name__ == "__main__":
    run()
