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
    # solutions = [
    #     {
    #         "name":"qa-201700920-testing",
    #         "sid":"a4ef6lxbjcfc00000"
    #     },
    #     {
    #         "name":"qa-201700920-testing-02",
    #         "sid":"e30n8hb5770800000"
    #     },
    #     {
    #         "name":"qa-201700920-testing-03",
    #         "sid":"n4qaa4vky5r000000"
    #     },
    #     {
    #         "name":"qa-201700920-testing-04",
    #         "sid":"w3y4e5fzieck00000"
    #     },
    #     {
    #         "name":"qa-201700920-testing-05",
    #         "sid":"t3h0n0p4bb3g00000"
    #     },
    #     {
    #         "name":"qa-201700920-testing-06",
    #         "sid":"l2wxebn01cts00000"
    #     },
    #     {
    #         "name":"qa-201700920-testing-07",
    #         "sid":"c50r06atnz0000000"
    #     },
    #     {
    #         "name":"qa-201700920-testing-08",
    #         "sid":"y4px4votkm3s00000"
    #     }
    # ]
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
        # interval = (endTime - startTime)/(50000*50)
        # write(solutions, startTime, endTime, interval, "metric50", 50)
        host = 'https://{}.{}'.format(solutions['name'], biz_info['solution_host'])
        create_endpoint(biz_info, solutions['sid'])
        # exit()
        '''500 k'''
        print "500k with 10 Metrics and 2 tags"
        # retried = 0
        # while retried <= 3:
        #     out = query_and_wait(host, startTime, endTime, "metric10", 10)
        #     if out == 1:
        #         break
        #     else:
        #         retried = retried + 1
        # '''50 M'''
        # print "50M with 10 Metrics and 2 tags"
        # retried = 0
        # while retried <= 3:
        #     out = query_and_wait(host, startTime, endTime, "metric10", 10)
        #     if out == 1:
        #         break
        #     else:
        #         retried = retried + 1
        
        '''5 G'''
        print "5G with 10 Metrics and 2 tags"
        retried = 0
        while retried <= 3:
            out = query_and_wait(host, startTime, endTime, "metric10", 10)
            if out == 1:
                break
            else:
                retried = retried + 1
        
        # '''5 G'''
        # print "5G with 50 Metrics and 2 tags"
        # retried = 0
        # while retried <= 3:
        #     out = query_and_wait(host, startTime, endTime, "metric50", 50)
        #     if out == 1:
        #         break
        #     else:
        #         retried = retried + 1
    # def Merics10with5g(host, startTime, endTime):
    #     solutions = [
    #         {
    #             "name":"qa-201700920-testing",
    #             "sid":"a4ef6lxbjcfc00000"
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
    #     interval = (endTime - startTime)/(50000*10)
    #     write(host, solutions, startTime, endTime, interval, "metric10", 10)
    # def Merics1with5g(host, startTime, endTime):
    #     solutions = [
    #         {
    #             "name":"qa-201700920-testing",
    #             "sid":"a4ef6lxbjcfc00000"
    #         }
    #     ]
    #     interval = (endTime - startTime)/50000
    #     write(host, solutions, startTime, endTime, interval, "metric1", 1)
    startTime = 1505903659000
    endTime = 1537497255000
    print(getQueryBody("metric10", 10, startTime, endTime))
    # single_export_size(biz_info, startTime, endTime)
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
        print "  Query Data: {}".format(json.dumps(data))
        request = readData(host + '/tsdb/export', data)
        s_t = time.time()
        if 'job_id' in request:
            print " Request ID: {}".format(request)
        else:
            print "{}".format(request)
    # response = requests.get(
    #     host+'/content/list', 
    #     headers={'content-type': 'application/json'}
    # )
    # print response.content
    
    complete = None
    print "Start To Ping Data, Please wait it complete...."
    while not complete:
        time.sleep(5)
        print "start get data"
        process_info = readData(host+'/tsdb/export/exportJobInfo', json.loads(request))
        print "==0?"
        if process_info == 0:
            print "==0 continue"
            continue
        print "convert info"
        process_info = json.loads(process_info)
        if 'state' not in process_info:
            continue
        e_t = time.time()
        state = process_info['state']
        if state == 'completed':
            complete = 1
        elif state == 'failed':
            print "Export Failed"
            complete = 2
            # if clear_content(host) == 1:
                # complete = 2 
    spend = e_t - s_t
    print "Spend time: {}".format(spend)
    return complete
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
def create_endpoint(biz_info, solution_id):
    endpoint = [
        {
            'method':'post',
            'path': '/tsdb/export',
            'script':'return Tsdb.export(request.body)'
        },
        {
            'method':'post',
            'path': '/tsdb/export/exportJobInfo',
            'script':'return Tsdb.exportJobInfo(request.body)'
        },
        {
            'method':'post',
            'path': '/content/download',
            'script':'return Content.download(request.body)'
        },
        {
            'method':'get',
            'path': '/content/clear',
            'script':'return Content.clear()'
        },
        {
            'method':'get',
            'path': '/content/list',
            'script':'return Content.list()'
        },
        {
            'method':'get',
            'path': '/tsdb/export/list',
            'script':'return Tsdb.exportJobList()'
        },
        {
            'method':'get',
            'path': '/tsdb/listMetric',
            'script':'return Tsdb.listMetrics()'
        }
    ]
    endpoint_host = "https://{}/api:1/solution/{}/endpoint".format(biz_info['biz_host'], solution_id)
    header={
        'content-type': 'application/json',
        'Authorization': str(biz_info['basic_authorization'])
    }
    for i in endpoint:
        response = requests.get(endpoint_host, headers=header)
        if response.status_code != 200:
            print "Get endpoint from biz failed {}: {}".format(response.status_code, response.content)
            exit()
        resp = json.loads(response.content)
        existing_path = filter(lambda existing: existing['path'] == i['path'], resp)
        if existing_path:
            continue
        print "Create Endpoint"
        response = requests.post(endpoint_host, headers=header, data=json.dumps(i))
        if response.status_code == 200:
            print "Create {} Enpoint Pass".format(i['path'])
        else:
            print "Create Enpoint Failed, Because Of {}".format(response.content)
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
if __name__ == '__main__':
    main()