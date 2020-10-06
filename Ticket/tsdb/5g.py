import ast
import requests
import os
import sys
import base64
import json
import time
import subprocess
import random
import math

def main():
    # host = "localhost:4000"
    biz_info = {
        "basic_authorization": "Basic bmluYXpoYW5nK3ByZXZpZXdAZXhvc2l0ZS5jb206bmluYXpoYW5nK3ByZXZpZXc=",
        "biz_host": "bizapi-staging-preview.hosted.exosite.io",
        "solution_host": "apps.preview.exosite-staging.io"
    }

    def single_export_size(biz_info, startTime, endTime):
        '''
            Export performance - single export
            Data schema: 10 Metrics and 2 tags
            500 KB, 50 MB, 5 GB
        '''
        solutions = {
                "name":"qa-201700920-testing-09",
                "sid":"splj3wpelozk0000"
            }
        host = 'https://{}.{}'.format(solutions['name'], biz_info['solution_host'])
        
        # one solution many times
        # retried = 1
        # while retried <= 1:
        #     print("{}:".format(retried))
        #     out = query_and_wait(host, startTime, endTime, "metric50", 50)
        #     retried = retried + 1

        # one solution list all status
        # data=getData(host+'/tsdb/export/list')
        # i=0
        # data=json.loads(data)
        # while i<len(data):
        #     if data[i].get('state')!="enqueued":
        #         print(data[i].get('state'))
        #         # break
        #     i=i+1

        # print("current {}".format(i))
        # print(len(length))

        # data=getData(host+'/tsdb/export/list')
        # data=json.loads(data)
        # print(data[0]['state'])

        # data=readData(host+'/tsdb/export/exportJobInfo',{"job_id":"BxpKuW3XTzViMiXj2FIXPYwVo4Sdx5_wnmHHkNvLOMuuAv9WzNTUAOMEGyiBxnhk_shqM_B2ld1_H0pnTOOm6OwISMc6wWxJaem2zikMtUQUpexNcFDi6ajH7Nttz6uf"})
        # data=json.loads(data)
        # print(data)


        solutions = [
            {
                "name":"qa-201700920-testing-09",
                "sid":"splj3wpelozk0000"
            },
            {
                "name":"qa-201700920-testing-02",
                "sid":"e30n8hb5770800000"
            },
            {
                "name":"qa-201700920-testing-03",
                "sid":"n4qaa4vky5r000000"
            },
            {
                "name":"qa-201700920-testing-04",
                "sid":"w3y4e5fzieck00000"
            },
            {
                "name":"qa-201700920-testing-05",
                "sid":"t3h0n0p4bb3g00000"
            },
            {
                "name":"qa-201700920-testing-06",
                "sid":"l2wxebn01cts00000"
            },
            {
                "name":"qa-201700920-testing-07",
                "sid":"c50r06atnz0000000"
            },
            {
                "name":"qa-201700920-testing-08",
                "sid":"y4px4votkm3s00000"
            }
        ]
        requestid=[{"job_id":"88YCx7v75g9CcRcobAAQmlJ7wF57MJb2j.35T9uO4tNMsKMS5l01uR8aLSeMFXJ2KWkHdL.N08TbgHah_Xec9_E4Qom6vuomzCDKIrFdA6zax1p1XPwBPteIRy0dN4QZ"}]
        
        #search one
        # host = 'https://{}.{}'.format(solutions[0]['name'], biz_info['solution_host'])
        # data=readData(host+'/tsdb/export/exportJobInfo',requestid[0])
        # data=json.loads(data)
        # print(data['length'])
        
        # many solution one times
        retried = 1
        index=0
        # while index < len(solutions):
        #     host = 'https://{}.{}'.format(solutions[index]['name'], biz_info['solution_host'])
        #     out = query_and_wait(host, startTime, endTime, "metric10", 10)
        #     index=index+1

        # many solution list one status
        # print(data[1])
        # print(data[1].get('state'))
        # while index < len(solutions):
        #     host = 'https://{}.{}'.format(solutions[index]['name'], biz_info['solution_host'])
        #     data=getData(host+'/tsdb/export/list')
        #     data=json.loads(data)
        #     i=0
        #     # while data[i].get('job_id')!=requestid[index].get('job_id'):
        #     #     i=i+1
        #     # print("{}:{}".format(index,data[i].get('job_id')))
        #     print("{}:{}".format(index,data[i].get('state')))
        #     index=index+1
        # print("current {}".format(i))
        
        

    startTime = 1505903659000
    endTime = 1537497255000
    single_export_size(biz_info, startTime, endTime)
    # Merics50with5g(host, startTime, endTime)
    # Merics1with5g(host, startTime, endTime)
    # Merics10with5g(host, startTime, endTime)
    # query(host, sid, startTime, endTime, interval)
def getQueryBody(metricName, count, start_time, end_time):
    metrics = {}
    query = []
    for i in range(1, int(count)+1, 1):
        query.append("{}_{}".format(metricName, i))
    query = {
        'metrics': query,
        'tags': {
            'exp_Metric_N': str(count),
            'exp_Name': metricName
        },
        'start_time': start_time,
        'end_time': end_time
    }
    data = {
        'query':query,
        'filename': 'qa_export'
    }
    return data

def query_and_wait(host, startTime, endTime, metricName, count):
    request = None
    while not request:
        data = getQueryBody(metricName, count, startTime, endTime)
        # print "  Query Data: {}".format(json.dumps(data))
        request = readData(host + '/tsdb/export', data)
        s_t = time.time()
        if 'job_id' in request:
            print " Request ID: {}".format(request)
        else:
            print "{}".format(request)

    
def clear_content(host):
    response = requests.get(
        host+'/content/clear', 
        headers={'content-type': 'application/json'}
    )
    print response.status_code
    if response.status_code == 200:
        print "Clear the content"
        return 1
    return 0

def readData(host, data):
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
            host,
            headers=HEADER,
            data=json.dumps(data)
        )
    except Exception, e:
        print "Connect Error({}): {}".format(e.errno, e.strerror)
    else:
        if response.status_code == 200:
            requestResult = response.content
        else:
            print "## Get error {}".format(response.content)
    return requestResult

def getData(host):
    '''
    random.seed(i)
    data = getRandomData()
    writeData(data)
    return (1 ok, 0 fail)
    '''
    HEADER = {'content-type': 'application/json'}
    requestResult = 0
    try:
        response = requests.get(
            host,
            headers=HEADER
        )
    except Exception, e:
        print "Connect Error({}): {}".format(e.errno, e.strerror)
    else:
        if response.status_code == 200:
            requestResult = response.content
        else:
            print "## Get error {}".format(response.content)
    return requestResult
if __name__ == '__main__':
    main()