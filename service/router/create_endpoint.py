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


def main():
    # sid = input("solutionID? ")
    host = "bizapi-staging.hosted.exosite.io/api:1/solution"
    solution = {
        "sid": "w3q6p1wzyt9800000"
    }
    # solution = {
    #     "sid": "z3o3l1mca5xy00000"
    # }

    createEndpoint(host, solution, 0, 550)


def getData():
    size = random.randint(1, 40)
    name = ''.join(random.choice(
        string.ascii_lowercase) for _ in range(size))
    data = {
        "method": "get",
        "path": "/{}".format(name),
        "script": ""
    }
    return data


def saveResult(data):
    timestamp = int(round(time.time() * 1000))
    result_path = "results_{}.txt".format(timestamp)
    print result_path
    try:
        f = open(result_path, "w")
        try:
            f.write(data)  # Write a string to a file
        finally:
            f.close()
    except IOError:
        pass


def createEndpoint(host, solution, start, end):
    data = ""
    # for x in xrange(start, end):
    #     size = getEndpointCount(host, solution['sid'])
    #     if size or size == 0:
    #         print "currently endpoint count :{}".format(size)
    #         data = "currently endpoint count :{}".format(size)

    size = getEndpointCount(host, solution['sid'])
    if size or size == 0:
        print "currently endpoint count :{}".format(size)
        data = "currently endpoint count :{}".format(size)
        for x in xrange(start, end):
            print "create enpoint....."
            print "Count: {}".format(size + x + 1)
            data = "--------------------\n" + data
            data = "\nCount: {}".format(x) + data
            router = getData()
            resp = postData(host, solution['sid'], router)
            print resp.content
            data = str(router) + data
            data = resp.content + data
            data = "--------------------\n" + data
            time.sleep(1)
        saveResult(data)


def postData(host, sid, data):
    '''
    random.seed(i)
    data = getRandomData()
    writeData(data)
    return (1 ok, 0 fail)
    '''
    HEADER = {'content-type': 'application/json',
              'Authorization': 'Basic dGVzdGluZ0BleG9zaXRlLmNvbToxMjM0ZXN6eGN2Kys='}
    requestResult = 0
    try:
        response = requests.post(
            "https://{}/{}/endpoint".format(host, sid),
            headers=HEADER,
            data=json.dumps(data)
        )
        return response
    except Exception, e:
        requestResult = 0
        print e


def getEndpointCount(host, sid):
    '''
    random.seed(i)
    data = getRandomData()
    writeData(data)
    return (1 ok, 0 fail)
    '''
    HEADER = {'content-type': 'application/json',
              'Authorization': 'Basic dGVzdGluZ0BleG9zaXRlLmNvbToxMjM0ZXN6eGN2Kys='}
    requestResult = 0
    try:
        response = requests.get(
            "https://{}/{}/endpoint".format(host, sid),
            headers=HEADER
        )
        if response.status_code != 200:
            print response
            print response.content
            return False
        else:
            return len(json.loads(response.content))
    except Exception, e:
        requestResult = 0
        print e

if __name__ == '__main__':
    main()
