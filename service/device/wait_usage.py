import requests
import json
import calendar
import time


def get_usage(url):
    payload = ""
    headers = {'content-type': 'application/json'}
    response = requests.request("GET", url, data=payload, headers=headers)
    usage = json.loads(response.text)
    return usage['device2']['usage']

url = "http://localhost:8081/api/v1/solution/b5bsxk62654g00000/usage"
usage = get_usage(url)
transacted_51 = usage['transacted_51']
transacted_1001 = usage['transacted_1001']
print "---------------------------"
print "Current transacted_51: {}".format(transacted_51)
print "Current transacted_1001: {}".format(transacted_1001)
print "---------------------------"
start = int(time.time()) + 960

while True:
    print "Wait usage update ...."
    time.sleep(5)
    resp = get_usage(url)
    end = int(time.time())
    if transacted_51 != resp['transacted_51']:
        print "transacted_51 is change..............."
    if transacted_1001 != resp['transacted_1001']:
        print "transacted_1001 is change..............."
    print "Times :{} s".format(end - start)
    time.sleep(5)
