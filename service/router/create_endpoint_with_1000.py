import requests
import os
import sys
import base64
import json
import time
import threading
import subprocess
import random
import math
import re
import signal
import string

# https://github.com/exosite/pegasus_api/blob/master/services/webservice.yaml#L762
def main():
    host = "https://bizapi-staging.hosted.exosite.io/api:1/solution"
    # host = "http://localhost:6000/api/v1/solution"
    solution = {
        "sid": "u58cvblvsrmk00000"
    }
    createEndpoint(host, solution,1000)


def getData(size):
    name = ''.join(random.choice(
        string.ascii_lowercase) for _ in range(size))
    data = {
        "method": "get",
        "path": "/{}".format(name),
        "script": ""
    }
    return data


def createEndpoint(host, solution,size):
    data = ""
    print "create enpoint....."
    router = getData(size)
    print router
    resp = postData(host, solution['sid'], router)
    print resp.content
    print resp.status_code
    if resp.status_code == 200:
        deleteData(host, solution['sid'], json.loads(resp.content)['id'])


def postData(host, sid, data):
    '''
    random.seed(i)
    data = getRandomData()
    writeData(data)
    return (1 ok, 0 fail)
    '''
    HEADER = {'content-type': 'application/json',
              'Authorization': 'Basic dGVzdGluZ0BleG9zaXRlLmNvbToxMjM0ZXN6eGN2Kys='}
    try:
        response = requests.post(
            "{}/{}/endpoint".format(host, sid),
            headers=HEADER,
            data=json.dumps(data)
        )
        return response
    except Exception, e:
        print e


def deleteData(host, sid, eid):
    HEADER = {'content-type': 'application/json',
              'Authorization': 'Basic dGVzdGluZ0BleG9zaXRlLmNvbToxMjM0ZXN6eGN2Kys='}
    try:
        response = requests.delete(
            "{}/{}/endpoint/{}".format(host, sid, eid),
            headers=HEADER
        )
        print response
        print response.content
    except Exception, e:
        print e

if __name__ == '__main__':
    main()
