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
            "name": "mur6094",
            "sid": "k2535ky8kss5c0000"
        }
    ]
    write(host, solutions, 0, 1002, "qa_metrics",1,0)
    # saveData(getData("qa_metrics",1,101))


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


def getData(metricName, metricsCount, tagsCount):
    metrics = {}
    tags = {}
    data = {}
    ary = []
    for x in xrange(0, metricsCount):
        file = os.urandom(5)
        file = base64.b64encode(file).decode('utf-8')
        metrics.update({"{}_{}".format(metricName, x): file})

    # for x in xrange(0, tagsCount):
    #     ary.append("{}_{}".format(metricName, x))
    # tags.update({metricName: ary})
    tags.update({metricName: "{}_{}".format(metricName, 2)})
    # data = {
    #     'metrics': [metricName],
    #     'tags': tags
    # }
    data = {
        'metrics': metrics,
        'tags': tags
    }
    print "Data: {}".format(data)
    return data


def write(host, solutions, start, end, metricName, metricsCount, tagsCount):
    for i in range(start, end, 1):
        out = 0
        while not out:
            print solutions
            for sid in solutions:
                # print sid
                out = fillData(host, sid['sid'], getData(
                    metricName, metricsCount, i))
        print "Count: {} ".format(i)


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
