from paho.mqtt import client as mqtt
import os
import ssl

# host = "zh4df5qjc8k80000.m2.exosite-staging.io"
host = "b53jw9xp93w800000.m2.preview.exosite-staging.io"
cert = "./trusted.crt"

def on_connect(client, userdata, flags, rc):
    resource = "$resource/" + input("Resource ID? ")
    client.publish(resource, input("Value? "), qos=0)
    client.disconnect()

def on_message(client, userdata, msg):
 print("Value set, previous was: ", msg.payload.decode())

def on_disconnect(client, userdata, rc):
    if rc == 0:
        print("Normal disconnected ", rc)
    if rc != 0:
        print("DisConnected with error", rc)
        exit()

client = mqtt.Client(client_id="")
cert_name="okami"
if cert_name:
    certfile = "./adc-cert.pem"
    keyfile  = "./adc-key.pem"
    print("Current dir: " + os.getcwd() + " Certificate: " + certfile + ", Keyfile: " + keyfile)
    client.tls_set(
        ca_certs=cert,
        server_hostname=host,
        certfile=certfile,
        keyfile=keyfile,
        cert_reqs=ssl.CERT_NONE
    )
client.tls_insecure_set(True)

client.on_connect = on_connect
client.on_disconnect = on_disconnect

client.connect(host, 443)
client.loop_forever()
