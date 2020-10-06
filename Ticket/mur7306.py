import requests
import json
import calendar
import time


solutionID = "q1kk83lk8gm0w0000"
headers = {'content-type': 'application/json',
           'authorization': 'Basic dGVzdGluZ0BleG9zaXRlLmNvbToxMjM0ZXN6eGN2Kys='}

name = str(int(time.time()))
print "create device..."
response = requests.request(
    'put', 'https://bizapi-staging.hosted.exosite.io/api:1/service/{}/device2/identity/{}'.format(
        solutionID, name), headers=headers)
if response.status_code != 204:
    raise Exception("create device fail {}".format(response.content))
else:
    print "device name: {}".format(name)

print "update device..."
expire_time = int(time.time() + 10) * 1000000
data = {"auth": {"expire": expire_time}}
response = requests.request(
    'patch', 'https://bizapi-staging.hosted.exosite.io/api:1/service/{}/device2/identity/{}'.format(
        solutionID, name),
    json=data, headers=headers)
if response.status_code != 204:
    raise Exception("update device fail {}".format(response.content))

print "wait until deivce is updated status..."
while True:
    response = requests.request(
        'get', 'https://bizapi-staging.hosted.exosite.io/api:1/service/{}/device2/identity/{}'.format(
            solutionID, name), headers=headers)
    
    device = response.json()
    end_time = int(time.time() + 10) * 1000000
    diff_time = (end_time - expire_time) / 1000000
    if device['status'] == 'expired':
        print "update success"
        print "-----------------------"
        print "expire_time : {} ".format(expire_time)
        print "device status updated_time : {} ".format(end_time)
        print "updating time: {}".format(diff_time)
        print "-----------------------"
        break
    else:
        print "device do not update after {}s".format(diff_time)
   	time.sleep(1)

print "delete device..."
response = requests.request(
    'delete', 'https://bizapi-staging.hosted.exosite.io/api:1/service/{}/device2/identity/{}'.format(
        solutionID, name), headers=headers)
if response.status_code != 205:
    raise Exception("delete device fail {}".format(response.content))
else:
    print "delete successfully"