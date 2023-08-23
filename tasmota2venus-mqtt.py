import random
import json

from paho.mqtt import client as mqtt_client


broker = '192.168.178.88'
port = 1883
topic = "tele/haushalt_/SENSOR"
topic_new = "power"
json_string = ""

frame = {}
grid = {}
L1 = {}
L2 = {}
L3 = {}

# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
# username = ''
# password = ''


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client, msg2):
        
        result = client.publish(topic_new, msg2)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(".")
        else:
            print(f"Failed to send message to topic {topic_new}")


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        json_object = json.loads(msg.payload.decode())
        if "leistung_gesamt" in json_object["haus"]:
            json_string = json_object["haus"]["leistung_gesamt"]
            json_formatted_str = json.dumps(json_string)
            grid["power"] = float(json_formatted_str)
        if "bezug" in json_object["haus"]:
            json_string = json_object["haus"]["bezug"]
            json_formatted_str = json.dumps(json_string)
            grid["energy_forward"] = float(json_formatted_str)
        if "einspeisung" in json_object["haus"]:
            json_string = json_object["haus"]["einspeisung"]
            json_formatted_str = json.dumps(json_string)
            grid["energy_reverse"] = float(json_formatted_str)
        if "leistung_L1" in json_object["haus"]:
            json_string = json_object["haus"]["leistung_L1"]
            json_formatted_str = json.dumps(json_string, indent=2)
            L1["power"] = float(json_formatted_str)
        if "leistung_L2" in json_object["haus"]:
            json_string = json_object["haus"]["leistung_L2"]
            json_formatted_str = json.dumps(json_string, indent=2)
            L2["power"] = float(json_formatted_str)
        if "leistung_L3" in json_object["haus"]:
            json_string = json_object["haus"]["leistung_L3"]
            json_formatted_str = json.dumps(json_string, indent=2)
            L3["power"] = float(json_formatted_str)

            
            frame["grid"] = "sampleData"
            frame["grid"] = grid
            frame["grid"]["L1"] = L1
            frame["grid"]["L2"] = L2
            frame["grid"]["L3"] = L3
 
            msg2 = json.dumps(frame)
            publish(client,msg2)
    
    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()