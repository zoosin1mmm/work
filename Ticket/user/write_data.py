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
from ExoSolution import *


def main():
    host = "stacy.apps.exosite-staging.io"
    solution = {
        "sid": "j31gs6zf6sm600000"
    }
    # print "create role..."
    # print(ExoSolution.create_role_via_api(
    #         solution['sid'], "guest", [{"name": "sn"},{"name": "location"}]))
    # print "create role..."
    # print(ExoSolution.create_role_via_api(
    #         solution['sid'], "admin", [{"name": "sn"},{"name": "location"}]))
    # print "create role..."
    # print(ExoSolution.create_role_via_api(
    # solution['sid'], "employee", [{"name": "sn"},{"name": "location"}]))

    # createUser(host, solution, 1, 21)

    assignUser(host, solution, "admin", "location", 1, 21)
    assignUser(host, solution, "admin", "sn", 1, 21)
    assignUser(host, solution, "guest", "location", 1, 21)
    assignUser(host, solution, "guest", "sn", 1, 21)
    assignUser(host, solution, "employee", "location", 1, 21)
    assignUser(host, solution, "employee", "sn", 1, 21)


def getData(size):
    size = random.randint(1, size)
    data = ''.join(random.choice(
        string.ascii_uppercase) for _ in range(size))
    return data


def saveResult(data):
    timestamp = int(round(time.time() * 1000))
    result_path = "data/results_{}.txt".format(timestamp)
    print result_path
    try:
        f = open(result_path, "w")
        try:
            f.write(data)  # Write a string to a file
        finally:
            f.close()
    except IOError:
        pass


def createUser(host, solution, start, end):
    data = ""
    for x in xrange(start, end):
        single = ""
        name = getData(20)
        email = "testing+" + getData(10) + "@exosite.com"
        password = "1234eszxcv++"
        print "create user....."
        ExoSolution.create_user_via_api(solution['sid'], name, email, password)
        userID = ExoSolution.get_user_id(solution['sid'], email)
        single = single + "-----------------------------------------\n"
        single = single + "Count : {}\n".format(x)
        single = single + "name :{}  \nemail:{} \npassword:{} \nuserID:{} \n".format(
            name, email, password, x)
        single = single + "-----------------------------------------\n"
        print single
        data = data + single
        time.sleep(1)
    saveResult(data)


def assignUser(host, solution, roleId, parameterName, start, end):
    data = ""
    all = ExoSolution.get_user_list_via_api(solution['sid'])
    for x in xrange(start, end):
        single = ""
        password = "1234eszxcv++"
        name = all[x]['name']
        email = all[x]['email']
        id = ExoSolution.get_user_id(solution['sid'], email)
        print "assign User....."
        parameters = []
        for i in xrange(start, end):
            parameters.append({"name": parameterName, "value": i})

        postData(host + "/assignUser",
                 {"id": id, "roles": [{"role_id": roleId, "parameters": parameters}]})
        single = single + "-----------------------------------------\n"
        single = single + "Count : {}\n".format(x)
        single = single + "name :{}  \nemail:{} \npassword:{} \nuserID:{} \nroleID: {} \nparameter_name:{}\n".format(
            name, email, password, x, roleId, parameterName)
        single = single + \
            "assignValue: name:{} value:{}~{}\n".format(
                parameterName, start, end)
        single = single + "-----------------------------------------\n"
        print single
        data = data + single
        time.sleep(1)
    saveResult(data)


def postData(host, data):
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
            "https://{}".format(host),
            headers=HEADER,
            data=json.dumps(data)
        )
        # print response.content
    except Exception, e:
        requestResult = 0
        print e
    else:
        print response.status_code
        if response.status_code == 204:
            requestResult = 1

    return requestResult

if __name__ == '__main__':
    ExoSolution = ExoSolution()
    main()
