import time

import paho.mqtt.client as mqtt

import mqtt_utils


client = mqtt.Client()
client.on_connect = mqtt_utils.on_connect
client.on_message = mqtt_utils.on_message
client.connect(mqtt_utils.BROKER_ADDRESS, mqtt_utils.BROKER_PORT)
client.loop_start()
while True:
    try:
        time.sleep(0.1)
    except KeyboardInterrupt:
        client.disconnect()
        client.loop_stop()
        break