import paho.mqtt.client as mqtt
import sys

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    sub = sys.argv[3] if len(sys.argv) > 3 else "$SYS/#"
    print("Subscribing to {}".format(sub))
    client.subscribe(sub)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client(client_id=(sys.argv[1] if len(sys.argv) > 2 else "bob"))
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("use-token-auth", (sys.argv[2] if len(sys.argv) > 2 else "bob123"))
client.connect("qwerty123.messaging.localhost", 80, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
