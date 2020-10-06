#!/usr/bin/env python
import json
import os
import requests
import sys
import time
import json
data = {
    "duration": 1000,
    "message": "testing"
}

SESSION = requests.Session()

SESSION.headers.update({
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjcsImlzcyI6Imh0dHA6Ly9zcGhpbngtdXNtOjMwMDAvYXBpL3YxL3VzZXIvbG9naW4iLCJpYXQiOjE1MjEwNzc5MTksImV4cCI6MTUyMzY2OTkxOSwibmJmIjoxNTIxMDc3OTE5LCJqdGkiOiJBQUJhVjJ6NzVxVFNGT3p3In0.54lhnV28XTYOUzbrsh71SbWCfuNVOstT64va_zBZ0hc"
})
while True:
    start = int(time.time())
    resp = SESSION.request(
        "post", "https://mur6094.apps.exosite-staging.io/timer", json=data)
    end = int(time.time())
    print resp.json()
    print "spend time {}".format(str(end - start))
