import paho.mqtt.client as mqtt
import sys


def _getdef(arg, default):
    try:
        return sys.argv[arg]
    except IndexError:
        return default


user = _getdef(1, "use-token-auth")
pw = _getdef(2, "-ankVuPqceD(LBd0Zc")
sub = _getdef(3, "$SYS/#")
client_id = _getdef(4, "g:veejb5:novo-gateway:576127cb94149d536f8e6a93")

host = "mqtt.zoetrope.local"
port = 80


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
print(client.connect(host, port, 60))

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
