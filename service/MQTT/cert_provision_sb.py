from paho.mqtt import client as mqtt
import os
import subprocess
import ssl

cert = "./trusted.crt"


def create_certificate(file):
    subprocess.call(["openssl", "req", "-x509", "-nodes", "-days", "365",
                     "-sha256", "-subj", "/C=US/ST=MN/L=Mpls/O=Exosite/CN=" +
                     file, "-newkey", "rsa:2048", "-keyout",
                     file + "-key.pem", "-out", file + "-cert.pem"])


def on_connect(client, userdata, flags, rc):
    provision_str = "$provision"
    print("Connected; no need to publish to provision")
    client.disconnect()


def on_disconnect(client, userdata, rc):
    if rc == 0:
        print("Normal disconnected ", rc)
    if rc != 0:
        print("DisConnected with error", rc)
        exit()


env = input("ENV ? ( dev / staging / production ) ")
host = input("Product ID? ") + ".m2.exosite-" + str(env) + ".io"
file = str(input("device? "))
create_certificate(file)

client = mqtt.Client(client_id="")

certfile = file + "-cert.pem"
keyfile = file + "-key.pem"
print("Current dir: " + os.getcwd() + " Certificate: " +
      certfile + ", Keyfile: " + keyfile)
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
