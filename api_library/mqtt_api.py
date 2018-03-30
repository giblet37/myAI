

import settings
from classes.api import Api
import paho.mqtt.client as mqtt
import log
import AI
from threading import Thread
import json
from functions import tts
import re


class MQTTApi(Api):

    def __init__(self):
        super(MQTTApi, self).__init__('mqtt')

    #@classmethod
    def publish_item(self, topic, message=None):
        #log.info("MQTT Published - Topic: {} Message: {}".format(topic,message))
        self.client.publish(topic, payload=message, qos=1)

    def register_callback(self):
        pass

    def on_connect(client, userdata, rc):
        #log.debug("MQTT connected with result code " + str(rc))
        #client.subscribe("hermes/tts/say")
        client.subscribe("hermes/audioServer/+/playFinished")
        client.subscribe("hermes/intent/#")


    def on_message(client, userdata, msg):
        #log.info("MQTT on_message: " +msg.topic + " " + str(msg.payload))
        #reg = r"hermes/audioServer/.+/playFinished"
        if msg.topic == 'hermes/tts/say':
            t = Thread(target=tts.speak, args=( msg.payload,))
            t.start()   #this runs the MAC say function to talk
        elif re.match(r"hermes/audioServer/.+/playFinished", msg.topic, flags=0):
            data = json.loads(msg.payload)
            rev = data['id']
            rev = rev[::-1] #reversed back from the speak tts.py
            newstr = "{\"id\":\"" + rev + "\",\"sessionId\":null}"
            client.publish('hermes/tts/sayFinished', payload=newstr, qos=1)
        elif msg.topic is not None and msg.topic.startswith("hermes/intent/") and msg.payload:
            print("intent message")
            AI.inst.parse_intent(msg.payload)


    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    log.info("MQTT Connecting... {}:{}".format(settings.MQTT_SERVER, settings.MQTT_PORT))
    client.connect(settings.MQTT_SERVER, settings.MQTT_PORT, 60)

    client.loop_start()

    