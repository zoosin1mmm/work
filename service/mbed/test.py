import json
import os
import sys
import subprocess
import requests


class ExoMbed(object):

    def __init__(self):
        # try:
        #     self.BuiltIn = BuiltIn()
        # except:
        #     print('import BuiltIn failed')

        self.SESSION = requests.Session()
        self.TOKEN = None
        self.SESSION.headers = {
            'Content-Type': 'text/plain',
            'Accept': 'application/json'
        }

    def __request(self, method, append='', **kwargs):
        resp = self.SESSION.request(
            method, 'https://api.connector.mbed.com/v2{append}'.format(**locals()), **kwargs)
        return resp

    def __headers(self, token=None):
        if token is None:
            if self.TOKEN is None:
                self.TOKEN = 'LM3NAULhO0VLikCtTUS4sMxJTPhJzzYT4xtAF1Z8IJirpsAHr9O1nHUdGK5RK2DcZgMR3anvqUeyRFRwHCT7DQ0n99oLNLYMopEq'
            token = self.TOKEN
        self.SESSION.headers.update(
            {'authorization': 'Bearer {token}'.format(**locals())})

# -------------------------------------------
    def mbed_call_back(self, token=None):
        self.__headers(token)
        resp = self.__request(
            'get', "/notification/callback")
        if resp.status_code != 200:
            return resp
        return resp.json()

    def mbed_device_create(self, deviceNum=1):
        subprocess.call(["docker", "build", "-t=device", os.path.join(
            os.path.dirname(os.path.abspath(__file__)), './mbed-simulators', '.')])
        docker_cmd = ["docker", "run", "-d", "device", "python",
                      "device.py", "{deviceNum}".format(**locals())]
        try:
            subprocess.check_call(docker_cmd)
        except Exception, e:
            print str(e)

    def mbed_device_stop_send_data(self):
        container = subprocess.Popen(
            ["docker", "ps", "-a", "-q"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if not container.stdout.read():
            print str('No Container')
        else:
            os.system('docker rm -f $(docker ps -a -q)')

    def mbed_device_unregistered(self, token=None):
        session = requests.Session()

        data = self.mbed_call_back(token)
        exositeToken = data['headers']['X-Exosite-Token']
        url = data['url']
        deviceList = self.mbed_endpoint_list()
        session.headers = {
            'x-exosite-token': '{exositeToken}'.format(**locals()),
            'Content-Type': 'application/json'
        }

        for x in range(0, len(deviceList)):
            device = deviceList[x]['name']
            print({"de-registrations": ["{device}".format(**locals())]})
            resp = session.request(
                'put', url, json={"de-registrations": ["{device}".format(**locals())]})

        self.mbed_device_stop_send_data()
        return resp

    def mbed_endpoint_list(self, token=None):
        self.__headers(token)
        resp = self.__request(
            'get', "/endpoints/")
        if resp.status_code != 200:
            raise AssertionError(
                "Endpoint List Failed --> {resp.status_code}  {resp.content}".format(**locals()))
        return resp.json()

if __name__ == '__main__':
    ExoMbed = ExoMbed()
    command=str(sys.argv[1])
    if command=="create" or command=="c":
        print("Create device")
        ExoMbed.mbed_device_create()

    elif command=="u":
        print("Unregister device")
        ExoMbed.mbed_device_unregistered()

    elif command=="s" or command=="stop":
        print("Stop to send device")
        ExoMbed.mbed_device_stop_send_data()

    elif command=="l" or command=="list":
        print("List device")
        print(ExoMbed.mbed_endpoint_list())

    elif command=="cb" or command=="callback":
        print("Get mbed call back")
        print(ExoMbed.mbed_call_back())
        
    else:
        print("none")