from paho.mqtt import client as mqtt
import ssl
env = input("ENV ? ( dev / staging / production ) ")
host = input("Product ID? ") + ".m2.exosite-" + str(env) + ".io"

cert = "./trusted.crt"


def on_connect(client, userdata, flags, rc):
    print("On-connect return code: ", rc)
    provision_str = str("$provision/" + input("Username? "))
    password = str(input("Password? ")) 
    client.publish(provision_str, password, qos=0)
    # client.disconnect()

def on_message(client, userdata, msg):
    print("Provision succeeded!")
    print("Response payload: ", msg.payload.decode())
    client.disconnect()


def on_publish(client, userdata, mid):
    print("On published!")
    # client.disconnect()


def on_disconnect(client, userdata, rc):
    if rc == 0:
        print("Normal disconnected ", rc)
        exit()
    if rc != 0:
        print("Disconnected with return code:", rc)
        exit()

client = mqtt.Client(client_id="")
client.tls_set(
    ca_certs=cert,
    server_hostname=host,
    cert_reqs=ssl.CERT_NONE
)
client.tls_insecure_set(True)

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.on_publish = on_publish

client.connect(host, 443)
client.loop_forever()
