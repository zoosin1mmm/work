import requests
import json
import calendar
import time


host = "https://tsdb-5g-20170814.apps.exosite-staging.io/"
path = "tsdb/query"
method = "post"
# path = "listMetirc"
# method ="get"
url = host + path

payload = {
    "metrics": [
        "metric10_1",
        "metric10_10"
    ]
}
headers = {'content-type': 'application/json'}
count = 0
while True:
    response = requests.request(method, url, json=payload, headers=headers)
    print response
    print count
    count = count + 1
    time.sleep(0.5)
# print response.content
