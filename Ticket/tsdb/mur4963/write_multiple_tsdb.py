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
    global host
    global domain
    # domain = "stacy4.apps.exosite-staging.io/tsdb/write"
    # domain = "stacy4.apps.exosite-staging.io/tsdb/write2"
    domain = "teststacy.apps.exosite-staging.io/write"
    # domain = "teststacy.apps.exosite-staging.io/write2"
    # domain = "teststacy.apps.exosite-staging.io/write3"

    # host = "localhost:4000"
    # domain = "stacychen.apps.exosite-dev.io/write"
    # host = "pegasus-cass-service-dev.hosted.exosite.io"
    solution = {
        "name": "teststacy",
        "sid": "u58cvblvsrmk00000"
    }

    # solution = {
    #     "name": "stacychen",
    #     "sid": "xrv6xq7vzgz40000"
    # }

    # 400 {"result":null,"error":"Client Error: Exceeds maximum metric value size, 491520 bytes."}
    # write(solution,  "qa_metrics", 1, 0, 491520, 1)
    # 400 {"result":null,"error":"Client Error: Exceeds maximum number of data entries. [Max: 2000]"}
    # write(solution,  "qa_metrics", 1, 0, 5, 2001)
    # ts
    # [{"write_timestamp":1513669787791051},{"write_timestamp":1513669787791051}]
    # write(solution, "qa_metrics", metricsCount=1, tagsCount=0,
    # metricsSize=5, count=2,return_ts=True)



    # 102.4kb(102,394 bytes) limit file
    # results/post_results_1514346430089.txt
    # write(solution, 0, 1, "qa_metrics", metricsCount=1,
    #       tagsCount=0, metricsSize=100, count=2000, return_ts=False, saveDataY=1)

    # results/post_results_1514346580523.txt
    # write(solution, 0, 1,  "qa_metrics", metricsCount=100,
    #       tagsCount=0, metricsSize=100, count=20, return_ts=False, saveDataY=1)

    # results/post_results_1514345164315.txt
    # write(solution, 0, 1, "qa_metrics", metricsCount=1,
    #       tagsCount=20, metricsSize=100, count=95, return_ts=False, saveDataY=1)

    # results/post_results_1514345401426.txt
    # write(solution, 0, 1, "qa_metrics", metricsCount=100,
    #       tagsCount=19, metricsSize=100, count=1, return_ts=False, saveDataY=1)

    # results/post_results_1514345732564.txt
    write(solution, 0, 1, "qa_metrics", metricsCount=10,
    tagsCount=5, metricsSize=100, count=33, return_ts=False, saveDataY=1)


def write(solution, start, end, metricName, metricsCount, tagsCount, metricsSize, count, return_ts=False, saveDataY=0):
    response = ""
    data = ""
    avg_time = 0
    # print "----------------------------------------"
    # print "-------------Call PegasusAPI------------"
    # print "----------------------------------------"
    # for x in xrange(start, end):
    #     print "Count: {}" .format(x)
    #     postData = getData(
    #         metricName, metricsCount, tagsCount, metricsSize, count, return_ts)
    #     startTime = time.time()
    #     response = postMultiDataVaiPegasus(solution['sid'], postData)
    #     all = time.time() - startTime
    #     avg_time = avg_time + all
    #     post_path = saveData(postData,saveDataY)
    #     data = addResult(solution, metricName, metricsCount,
    #                      tagsCount, metricsSize, count, response, all, post_path) + data
    # avg_time = float(avg_time / (end - start))
    # saveResult(data, avg_time)
    print "----------------------------------------"
    print "-------------Call BizAPI----------------"
    print "----------------------------------------"
    avg_time = 0
    for x in xrange(start, end):
        print "Count: {}" .format(x)
        postData = getData(
            metricName, metricsCount, tagsCount, metricsSize, count, return_ts)
        response = postMultiDataVaiBiz(postData)
        post_path = saveData(postData, saveDataY)
        avg_time = avg_time + convertToInteger(response)
        data = addResult(solution, metricName, metricsCount,
                         tagsCount, metricsSize, count, response, convertToInteger(response), post_path) + data
        if response.status_code != 200:
            break
    avg_time = float(avg_time / (end - start))
    saveResult(data, avg_time)


def convertToInteger(resp):
    time = resp.content
    if time.find("error") == -1:
        if time.find("ms") != -1:
            time = time.strip('ms')
            time = float(time.strip()) / 1000
        elif time.find("s") != -1:
            time = time.strip('s')
            time = float(time.strip())
        else:
            time = 0
    else:
        time = 0
    return time


def saveData(postData, y):
    timestamp = int(round(time.time() * 1000))
    post_path = "data/post_body_{}.txt".format(timestamp)
    data = ""
    if y == 1:
        try:
            f = open(post_path, "w")
            try:
                f.write(json.dumps(postData))  # Write a string to a file
            finally:
                f.close()
        except IOError:
            pass
    return post_path


def addResult(solution, metricName, metricsCount, tagsCount, metricsSize, count, response, spendTime, post_path):
    data = ""
    data = data + "\n--------------------------------------------------\n"
    data = data + "solutionID: {} \n".format(solution['sid'])
    data = data + "Metirc: {} \nMetirc Size: {} \nMetirc length: {} \n".format(
        metricName, metricsCount, metricsSize)
    data = data + "Tags Size: {} \n".format(tagsCount)
    data = data + "Datapoint length: {} \n".format(count)
    data = data + "export post Data to {} \n".format(post_path)
    data = data + "Get Response: {} \n".format(response.content)
    data = data + "spend times : {} s\n".format(spendTime)
    data = data + "\n--------------------------------------------------\n"
    print data
    return data


def saveResult(data, avg_time):
    timestamp = int(round(time.time() * 1000))
    result_path = "results/post_results_{}.txt".format(timestamp)
    data = "Avg Spend time: {} \n".format(avg_time) + data
    print "Avg Spend time: {} \n".format(avg_time)
    print "export Results to {} \n".format(result_path)
    try:
        f = open(result_path, "w")
        try:
            f.write(data)  # Write a string to a file
        finally:
            f.close()
    except IOError:
        pass


def getData(metricName, metricsCount, tagsCount, metricsSize, count, return_ts):
    tags = {}
    data = {}
    datapoints = []
    byte = 0

    for x in xrange(0, tagsCount):
        tags.update({"{}_{}".format(metricName, x): str(metricName)})

    for x in xrange(0, count):
        metrics = {}
        for x in xrange(0, metricsCount):
            # 491520 480kb
            size = random.randint(1, metricsSize)
            # file = os.urandom(size)
            # file = base64.b64encode(file).decode('utf-8')
            file = ''.join(random.choice(
                string.ascii_uppercase + string.digits) for _ in range(size))
            byte = byte + sys.getsizeof(file)
            metrics.update({"{}_{}".format(metricName, x): str(file)})

        millis = int(round(time.time() * 1000))
        if tagsCount == 0:
            items = {
                "metrics": metrics,
                "ts": "{}ms".format(millis)
            }
        else:
            items = {
                "metrics": metrics,
                "tags":  tags,
                "ts": "{}ms".format(millis)
            }

        datapoints.append(items)

    data = {
        "datapoints": datapoints, "return_ts": return_ts
    }

    print "Data Size:{} byte".format(byte)
    return data


def postMultiDataVaiBiz(data):
    HEADER = {'content-type': 'application/json'}
    response = ""
    try:
        response = requests.post(
            "https://{}".format(domain),
            headers=HEADER,
            data=json.dumps(data)
        )
    except Exception, e:
        print e
        print "Connect Error({}): {}".format(e.errno, e.strerror)
    else:
        print response.status_code
        print response.content
    return response


def postMultiDataVaiPegasus(sid, data):
    HEADER = {'content-type': 'application/json'}
    response = ""
    try:
        response = requests.post(
            "http://{}/api/v1/timeseries/{}/multi_data".format(host, sid),
            headers=HEADER,
            data=json.dumps(data)
        )
    except Exception, e:
        print e
        print "Connect Error({}): {}".format(e.errno, e.strerror)
        subprocess.Popen(["oc", "project", "murano-staging"])
        time.sleep(5)
        subprocess.Popen(
            ["oc", "port-forward", "pegasus-cass-service-hopper", "4000"])
        time.sleep(5)
    else:
        print response.status_code
        print response.content

    return response

if __name__ == '__main__':
    main()
