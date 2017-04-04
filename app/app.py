import logging
import time
import string
import random
import json

from redis import Redis
from flask import Flask, request, jsonify
import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

mqttc = mqtt.Client(client_id="controller-{}".format(id_generator()))
app = Flask(__name__)
redis = Redis(host='redis', port=6379)



class InvalidClientId(Exception):
    pass


@app.route('/on_register', methods=['POST'])
def on_register():
    response = {
            "result": "next" 
    }

    client_id = request.json['client_id']

    if client_id.startswith('controller'):
        return jsonify(response)

    try:
        logger.info("New client: %s", convert_client_id_to_org_type_id(client_id))
    except InvalidClientId:
        logger.warning("Invalid client id received: %s", client_id)

    return jsonify(response)

@app.route('/auth_on_publish', methods=['POST'])
def auth_on_publish():
    response = {
            "result": "ok" 
    }
    logger.debug("Auth on publish")

    return jsonify(response)

@app.route('/auth_on_subscribe', methods=['POST'])
def auth_on_subscribe():
    response = {
            "result": "ok",
            "topics": request.json['topics']
    }
    logger.debug("Auth on susbcribe")

    return jsonify(response)

@app.route('/on_client_gone', methods=['POST'])
def on_client_gone():
    response = {
            "result": "next" 
    }

    logger.info("Client Disconnect: %s", request.json['client_id'])

    exit_handler()

    return jsonify(response)

@app.route('/on_client_offline', methods=['POST'])
def on_client_offline():
    response = {
            "result": "next" 
    }
    
    logger.info("Client Disconnect: %s", request.json['client_id'])
    
    exit_handler()

    return jsonify(response)

def build_connect_status_payload():
    """
    Build the connect status payload. It seems as though this is optional however the 
    following keys are listed in the IBM documentation

        {
            'ClientAddr': '195.212.29.68', 
            'Protocol': 'mqtt-tcp', 
            'ClientID': 'd:bcaxk:psutil:001', 
            'User': 'use-token-auth', 
            'Time': '2014-07-07T06:37:56.494-04:00', 
            'Action': 'Connect', 
            'ConnectTime': '2014-07-07T06:37:56.493-04:00', 
            'Port': 1883
        }

    For now, this is empty.
    """
    return json.dumps({})

def build_disconnect_status_payload():
    """
    Build the disconnect status payload. It seems as though this is optional however the 
    following keys are listed in the IBM documentation.

    The disconnect status can include all keys from the connect status

        {
            'WriteMsg': 0, 
            'ReadMsg': 872, 
            'Reason': 'The connection has completed normally.', 
            'ReadBytes': 136507, 
            'WriteBytes': 32, 
        }

    For now, this is empty.
    """
    return json.dumps({})

def exit_handler():
    logger.debug("Exit Handler")
    
    client_id = request.json['client_id']

    if client_id.startswith('controller'):
        return 

    try:
        org, device_type, device_id = convert_client_id_to_org_type_id(client_id)
    except InvalidClientId:
        logger.warning("Invalid Client Id: %s", client_id)
        return

    topic = "iot-2/type/{}/id/{}/mon".format(device_type, device_id)

    payload = build_disconnect_status_payload()
    logger.debug("Publishing MQTT")
    mqttc.publish(topic, payload)

def convert_client_id_to_org_type_id(client_id):
    """
    Client ID should be a string:
        "g:" + self._options['org'] + ":" + self._options['type'] + ":" + self._options['id'],

    """
    split = client_id.split(':')
    
    if len(split) != 4:
        raise InvalidClientId()

    org = split[1]
    device_type = split[2]
    device_id = split[3]

    return (org, device_type, device_id)

def mqtt_log(client, userdata, level, buf):
    logger.info("MQTT: %s", buf)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # Connect
    try:
        mqttc.connect("vernemq", 1883, 60)
    except:
        logger.warning("Could not connect to vernemq")
        #time.sleep(2)
    else:
        #logger.info("Connected to vernemq")
        #break
        pass
    mqttc.on_log = mqtt_log
    mqttc.loop_start()

    app.run(host="0.0.0.0", debug=True)
