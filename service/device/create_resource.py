import requests
import json
import time
import random
import string


def main():
    # projectId = "b5bsxk62654g00000"
    # env = "staging"

    projectId = "n1rzjq469jvog0000"
    env = "dev"
    host = "https://bizapi-{env}.hosted.exosite.io/api:1/service/{projectId}/device2".format(
        **locals())

    # create_one_resoure(host,"r_51_biz")
    # create_one_resoure(host,"r_1001")
    # create_one_resoure(host,"r_51")
    # create_resoure(host, 0, 50)
    # delete_all_resoure(host)


def create_one_resoure(host, name):
    data = {
        "resources": {
            "{}".format(name): {
                "format": "string",
                "settable": True,
                "allowed": []
            }
        }
    }
    print "Resource: {}".format(name)
    resp = post_request(host, data)
    print resp
    print resp.content


def getData(index):
    print "Resource: r_{}".format(x)
    return {"resources": {"r_{}".format(x): {"format": "string", "settable": True, "allowed": []}}}


def create_resoure(host, start, end):
    for x in xrange(start, end):
        print "------------------------"
        print "Count: {}".format(x)
        resource = getData(x)
        print "create resource"
        response = post_request(host, resource)
        print response
        print response.content
        print "------------------------"


def delete_all_resoure(host):
    response = get_resoure_list(host)
    data = response.json()
    for i in xrange(len(data["resources"])):
        resp = delete_resoure(host, data["resources"].keys()[i])
        print resp


def get_resoure_list(host):
    HEADER = {'content-type': 'application/json',
              'Authorization': 'Basic dGVzdGluZ0BleG9zaXRlLmNvbToxMjM0ZXN6eGN2Kys='}
    try:
        response = requests.get(
            "{host}".format(**locals()),
            headers=HEADER
        )
        return response
    except Exception, e:
        print e


def delete_resoure(host, resource):
    HEADER = {'content-type': 'application/json',
              'Authorization': 'Basic dGVzdGluZ0BleG9zaXRlLmNvbToxMjM0ZXN6eGN2Kys='}
    try:
        response = requests.delete(
            "{host}/{resource}".format(**locals()),
            headers=HEADER
        )
        print response
    except Exception, e:
        print e


def post_request(host, data):
    HEADER = {'content-type': 'application/json',
              'Authorization': 'Basic dGVzdGluZ0BleG9zaXRlLmNvbToxMjM0ZXN6eGN2Kys='}
    response = ''
    try:
        response = requests.patch("{host}".format(**locals()),
                                  headers=HEADER,
                                  data=json.dumps(data)
                                  )
    except Exception, e:
        print e
    return response

if __name__ == '__main__':
    main()
