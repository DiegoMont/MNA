BROKER_ADDRESS: str = "broker.hivemq.com"
BROKER_PORT: int = 1883

ALL_TOPICS = "MNA/Equipo33/#"
TOPIC_DIEGO = "MNA/Equipo33/DiegoMontaño-Humedad"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(ALL_TOPICS)

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))