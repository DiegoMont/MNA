import random
import time

import paho.mqtt.client as mqtt

import mqtt_utils


client = mqtt.Client()
client.on_connect = mqtt_utils.on_connect
client.connect(mqtt_utils.BROKER_ADDRESS, mqtt_utils.BROKER_PORT)
client.loop_start()
while True:
    try:
        temp = random.randint(25, 30)
        client.publish(mqtt_utils.TOPIC_DIEGO, temp, qos=0)
        time.sleep(10)
    except KeyboardInterrupt:
        client.disconnect()
        client.loop_stop()
        break