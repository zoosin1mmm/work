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

host = "https://bizapi-staging.hosted.exosite.io/api:1"
HEADER = {
    'content-type': 'application/json',
    'Authorization': 'Basic dGVzdGluZ0BleG9zaXRlLmNvbToxMjM0ZXN6eGN2Kys='
}
response = {}
try:
    response = requests.get(
        "{}/solution/k4x5s14xhjca00000/library/".format(host), headers=HEADER)
except Exception, e:
    print e

module = response.json()

for m in module["items"]:
	print(m)
	try:
		response = requests.delete(
		    "{}/solution/{}/library/{}/".format(host,
		                                        "k4x5s14xhjca00000", m["name"]),
		    headers=HEADER
		)
		print response
		print response.content
	except Exception, e:
		print e
