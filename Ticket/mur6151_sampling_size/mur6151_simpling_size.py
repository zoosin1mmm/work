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


def main():
    host = "localhost:4000"

    solutions = [
        {
            "name": "stacy3",
            "sid": "h1j04ugyb1tsw0000"
        }
    ]
    timestamp = int(time.time())
    print "now {} ".format(timestamp)
    write(host, solutions, 20, "qa", 1, timestamp)


def saveData(postData):
    timestamp = int(round(time.time() * 1000))
    post_path = "post_body_{}.txt".format(timestamp)
    data = ""
    try:
        f = open(post_path, "w")
        try:
            f.write(json.dumps(postData))  # Write a string to a file
        finally:
            f.close()
    except IOError:
        pass


def getData(metricName, metricsCount, tagsCount, i, timestamp):
    metrics = {}
    tags = {}
    data = {}
    ary = []
    for x in xrange(0, metricsCount):
        # file = os.urandom(5)
        # file = base64.b64encode(file).decode('utf-8')
        num = random.randint(1, 100000)
        metrics.update({"{}_{}".format(metricName, x): num})

    # for x in xrange(0, tagsCount):
        # ary.append("{}_{}".format(metricName, x))
    # tags.update({metricName: "{}_{}".format(metricName, tagsCount)})

    for x in xrange(0, tagsCount):
        tags.update({"{}_{}".format(metricName, x): "{}_{}".format(metricName, x)})

    data = {
        'metrics': metrics,
        'tags': tags,
        'ts': "{}s".format(timestamp)}
    print "Data: {}".format(json.dumps(data))
    return data


def write(host, solutions, end, metricName, days, timestamp):
    print "---------------"
    print "now -{} days".format(days)
    print "---------------"
    interval = 24 * 60 * 60 * days
    timestamp = timestamp - interval
    for i in range(0, end):
        timestamp = timestamp + i
        out = 0
        print "Count: {} ".format(i)
        while not out:
            print solutions
            for sid in solutions:
                # print sid
                out = fillData(host, sid['sid'], getData(
                    metricName, 1, 1, i, timestamp))


def fillData(host, sid, data):
    '''
    random.seed(i)
    data = getRandomData()
    writeData(data)
    return (1 ok, 0 fail)
    '''
    HEADER = {'content-type': 'application/json'}
    requestResult = 0
    try:
        response = requests.post(
            "http://{}/api/v1/timeseries/{}/data".format(host, sid),
            headers=HEADER,
            data=json.dumps(data)
        )
        # response = requests.delete(
        #     "http://{}/api/v1/timeseries/{}/delete_all".format(host, sid),
        #     headers=HEADER,
        # )
        print response.content
    except Exception, e:
        requestResult = 0
        print e
        print "Connect Error({}): {}".format(e.errno, e.strerror)
        subprocess.Popen(["oc", "project", "murano-staging"])
        time.sleep(5)
        subprocess.Popen(
            ["oc", "port-forward", "pegasus-cass-service-hopper", "4000"])
        time.sleep(5)
    else:
        print response.status_code
        if response.status_code == 204:
            requestResult = 1

    return requestResult
if __name__ == '__main__':
    main()
