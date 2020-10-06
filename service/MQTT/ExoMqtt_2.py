import os
import ssl
import time
import threading
from paho.mqtt import client as mqtt


class ExoMqtt(object):

    def __init__(self):
        self.message = {}
        self.thread_event = ""
        self.publish_data = {}
        self.publish_data['message'] = ""
        self.publish_data['topic'] = ""
        self.publish_data['qos'] = 0

    def close_loop(self, client):
        """ Close loop to MQTT server """
        print('end loop')
        self.thread_event.set()

    def message_clear(self):
        """ Clear all received messages"""
        self.message = {}

    def mqtt_connect(self, server="Test.mosquitto.org", user="", token=None, certfile=None, keyfile=None):
        """ Returns client object, starts an MQTT connection with server """
        print("creating new instance")
        cwd = os.path.dirname(os.path.abspath(__file__))
        # cert = os.path.join(cwd, "../res/mqtt/trusted.crt")
        cert = "./trusted.crt"
        client = mqtt.Client(client_id="")
        client.tls_set(
            ca_certs=cert,
            server_hostname=server,
            certfile=certfile,
            keyfile=keyfile,
            cert_reqs=ssl.CERT_NONE
        )
        client.tls_insecure_set(True)
        if token is not None:
            client.username_pw_set(user, token)
        print("connecting to broker")
        client.on_message = self.on_message
        client.on_disconnect = self.on_disconnect
        client.on_publish = self.on_publish
        client.on_connect = self.on_connect
        return client

    def mqtt_disconnect(self, client):
        """ Mqtt disconnect """
        print("Mqtt disconnect")
        client.disconnect()

    def mqtt_message(self):
        """ Returns all received MQTT messages """
        time.sleep(0.01)
        return self.message

    def mqtt_publish(self, client, topic, message=None, qos=0):
        """ Use mqtt protocol to activate the device """
        # client.publish(topic, message, qos=qos)
        self.publish_data['message'] = message
        self.publish_data['topic'] = topic
        self.publish_data['qos'] = qos

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print("DisConnected with error", rc)
            self.message['status_code'] = rc
            client.disconnect()

    def on_message(self, client, userdata, message):
        """ Saves message object when message is received called
        This is a callback function triggered when a message is received"""
        topic = str(message.topic)
        resp = {}
        resp['message'] = str(message.payload.decode("utf-8"))
        resp['qos'] = str(message.qos)
        resp['retain'] = str(message.retain)

        if topic in self.message:
            self.message[topic].append(resp)
        else:
            self.message[topic] = []
            self.message[topic].append(resp)
        self.message['status_code'] = 0

    def on_publish(self, client, userdata, mid):
        print("On published!")
        # client.disconnect()

    def on_connect(self, client, userdata, flags, rc):
        print("On-connect return code: ", rc)
        print("publish data: {} to topic: {}".format(self.publish_data['message'], self.publish_data['topic']))
        client.publish(self.publish_data['topic'], self.publish_data[
                       'message'], qos=self.publish_data['qos'])

    def start_loop(self, client):
        """ Start loop to MQTT server """
        print('start loop')
        self.thread_event = threading.Event()
        thread = threading.Thread(
            target=client.loop_forever, args=(1, self.thread_event))
        thread.start()
        time.sleep(1)

if __name__ == '__main__':
    env = input("ENV ? ( dev / staging / production ) ")
    host = input("Product ID? ") + ".m2.exosite-" + str(env) + ".io"
    ExoMqtt = ExoMqtt()
    client = ExoMqtt.mqtt_connect(host)
    provision_str = "$provision/" + input("Username? ")
    msg = str(input("Password? "))
    ExoMqtt.mqtt_publish(client, str(provision_str), msg.strip())
    client.connect(host, 443)
    ExoMqtt.start_loop(client)
    print(ExoMqtt.mqtt_message())
    ExoMqtt.close_loop(client)
    ExoMqtt.mqtt_disconnect(client)
