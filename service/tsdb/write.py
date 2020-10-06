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
    # def Merics50with5g(host, startTime, endTime):
    #     solutions = [
    #         {
    #             "name":"qa-201700920-testing-09",
    #             "sid":"splj3wpelozk0000"
    #         }
    #     ]
    #     num = 5e+9/(50000*50)
    #     interval = (endTime - startTime)/num
    #     pasr = 0*interval
    #     write(host, solutions, int(startTime+pasr), endTime, interval, "metric50", 50)

    # def Merics10with5g(host, startTime, endTime):
    #     solutions = [
    #         {
    #             "name":"qa-201700920-testing-09",
    #             "sid":"splj3wpelozk0000"
    #         },
    #         {
    #             "name":"qa-201700920-testing-02",
    #             "sid":"e30n8hb5770800000"
    #         },
    #         {
    #             "name":"qa-201700920-testing-03",
    #             "sid":"n4qaa4vky5r000000"
    #         },
    #         {
    #             "name":"qa-201700920-testing-04",
    #             "sid":"w3y4e5fzieck00000"
    #         },
    #         {
    #             "name":"qa-201700920-testing-05",
    #             "sid":"t3h0n0p4bb3g00000"
    #         },
    #         {
    #             "name":"qa-201700920-testing-06",
    #             "sid":"l2wxebn01cts00000"
    #         },
    #         {
    #             "name":"qa-201700920-testing-07",
    #             "sid":"c50r06atnz0000000"
    #         },
    #         {
    #             "name":"qa-201700920-testing-08",
    #             "sid":"y4px4votkm3s00000"
    #         }
    #     ]
    #     num = 5e+9/(50000*10)
    #     interval = (endTime - startTime)/num
    #     if sys.argv[2] == "c1":
    #         # 1-2000
    #         start = startTime
    #         # 1519833272831
    #         end = startTime + (2000*interval) # 1512222378200.0
    # write(host, solutions, int(start), int(end), int(interval), "metric10",
    # 10, , input_count=int(1))

    #     elif sys.argv[2] == "c2":
    #         # 2001-4000
    #         start = startTime + (2000*interval) # 1512222378200.0
    #         # Count: 1517656474480  save: 1860500000 bytes
    #         #                             100000000
    #         end = startTime + (4000*interval) # 1518541097400.0
    # write(host, solutions, int(start), int(end), int(interval), "metric10",
    # 10, , input_count=int(2000))

    #     elif sys.argv[2] == "c3":
    #         # 4001-6000
    #         start = startTime + (4000*interval) # 1518541097400.0
    #         # Count: 1524856656041  save: 100000000 bytes
    #         end = startTime + (6000*interval) # 1524859816600.0
    # write(host, solutions, int(start), int(end), int(interval), "metric10",
    # 10, , input_count=int(4000))

    #     elif sys.argv[2] == "c4":
    #         # 6001-8000
    #         start = startTime + (6000*interval) # 1524859816600.0
    #         # Count: 1531178534600  save: 100050000 bytes
    #         end = startTime + (8000*interval) # 1531178535800.0
    #         write(host, solutions, int(start), int(end), int(interval), "metric10", 10, , input_count=int(6000))
    #     elif sys.argv[2] == "c5":
    #         # 8001-10000
    #         start = startTime + (8000*interval) # 1531178535800.0
    #         # Count: 1531175375241  save: 100000000 bytes
    #         end = endTime
    #         write(host, solutions, int(start), int(end), int(interval), "metric10", 10, , input_count=int(8000))
    # def Merics1with5g(host, startTime, endTime):
    #     solutions = [
    #         {
    #             "name":"qa-201700920-testing-09",
    #             "sid":"splj3wpelozk0000"
    #         }
    #     ]
    #     # Count: 1506335858080  save: 1795000000 bytes
    #     # Count: 1516812894550  save: 1726550000 bytes
    #     # 64100/4 = 16025 801,250,000

    #     num = 5e+9/50000
    #     interval = (endTime - startTime)/num
    #     if sys.argv[2] == "c1":
    #         # start_from = 35900
    #         start = startTime + (35900*interval)
    #         end = startTime + (51925*interval)
    #         write(host, solutions, int(start), int(end), interval, "metric1", 1, input_count=int(35900))
    #     elif sys.argv[2] == "c2":
    #         start = startTime + (51925*interval)
    #         end = startTime + (67950*interval)
    #         write(host, solutions, int(start), int(end), interval, "metric1", 1, input_count=int(51925))
    #     elif sys.argv[2] == "c3":
    #         start = startTime + (67950*interval)
    #         end = startTime + (83975*interval)
    #         write(host, solutions, int(start), int(end), interval, "metric1", 1, input_count=int(67950))
    #     elif sys.argv[2] == "c4":
    #         start = startTime + (83975*interval)
    #         end = startTime + (100000*interval)
    #         write(host, solutions, int(start), int(end), interval, "metric1", 1, input_count=int(83975))
    
    # 204
    # Count: 1513749401510  save: 37300000 bytes
    # input_count:747
    # [{'name': 'tsdb-5g-20170814', 'sid': 'o11ykvtva1qvk0000'}]
    # {'name': 'tsdb-5g-20170814', 'sid': 'o11ykvtva1qvk0000'}
    # 50000 bytes
    # 204
    # Count: 1526541578326  save: 10150000 bytes
    # input_count:204
    # [{'name': 'tsdb-5g-20170814', 'sid': 'o11ykvtva1qvk0000'}]
    # {'name': 'tsdb-5g-20170814', 'sid': 'o11ykvtva1qvk0000'}
    # 50000 bytes
    # 204
    # Count: 1537497254326  save: 18800000 bytes
    # input_count:377
    # 1350.36551785
    # 377

    startTime = 1505903659000
    # startTime = 1513749401510
    # startTime= 1526541578326
    endTime = 1506020759000

    solutions = [
        {
            "name": "tsdb10000data",
            "sid": "d4gwmq3w7a8800000"
        }
    ]
    interval = (endTime - startTime) / 3159359.6 
    write(host, solutions, int(startTime),
          endTime, interval, "metric", 1)

    # if sys.argv[1] == "1":
    #     Merics1with5g(host, startTime, endTime)
    # elif sys.argv[1] == "10":
    #     Merics10with5g(host, startTime, endTime)
    # elif sys.argv[1] == "50":
    #     Merics50with5g(host, startTime, endTime)
    # else:
    #     print "select metrics number"


def get500MData(metricName, count, time):
    file = os.urandom(5)
    file = base64.b64encode(file).decode('utf-8')
    byte = sys.getsizeof(repr(file))
    print "{} bytes".format(byte*count)
    metrics = {}
    query = []
    for i in range(1, int(count) + 1, 1):
        metrics.update({"{}_{}".format(metricName, i): str(file)})
        query.append("{}_{}".format(metricName, i))
    data = {
        'metrics': metrics,
        'tags': {
            'exp_Name': "metric1"
        },
        'ts': time
    }
    return data


def write(host, solutions, startTime, endTime, interval, metricName, count, input_count=1):
    start = time.time()
    for i in range(startTime, endTime, int(interval)):
        # stog = 50000 * input_count
        stog = 5 * input_count
        out = 0
        while not out:
            print solutions
            for sid in solutions:
                print sid
                out = fillData(host, sid['sid'], i, metricName, count)
        print "Count: {}  save: {} bytes".format(i, stog)
        input_count = input_count + 1
        print "input_count:{}".format(input_count)
    all = time.time() - start
    print all
    print input_count


def fillData(host, sid, ts, metricName, count):
    '''
    random.seed(i)
    data = getRandomData()
    writeData(data)
    return (1 ok, 0 fail)
    '''
    HEADER = {'content-type': 'application/json'}
    data = get500MData(metricName, count, ts)
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
