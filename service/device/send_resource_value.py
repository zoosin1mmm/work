import requests
import json
import time
import random
import string


def main():
    projectId = "e28f0i8c3315w0000"
    env = "staging"
    # projectId = "n1rzjq469jvog0000"
    # env = "dev"

    bizapi_host = "https://bizapi-{env}.hosted.exosite.io/api:1".format(**locals())
    host = "https://{projectId}.m2.exosite-{env}.io".format(**locals())

    # dev
    # token_51 = "cd7exc36K5PBkdbKCrvO2oTmhJQ7Zirdyjwqn6TN"
    # staging
    # token_51 = "H4QxLXUkNl1qrbLfutKOS5K01mlN1YMWadQYFvnf"
    # token_1001 = "ii5maryKQuprjIjGPIJxTLpx4hZzN9UvjCgaxzVa"
    # token_51_pegasus = "g0uXMwkj8jO6zvsqQAydWVmXzGzhNJfX74lNUeYR"

    token="n4WCG9eFKiaKX9sbHTpKIyuAIaV47Ka9cJUmLGpu"
    send_value_to_resource(host, token, "test", 51)
    # send_value_to_resource(host, token_51, "r_51", 51)

    # send_value_to_resource_bizapi(
    #     bizapi_host, projectId, "device_50_pegasus", "r_51_pegasus", 51)
    # send_value_to_resource(host, token_1001, "r_1001", 1001)
    # resources = [
    #     "r_0"
    # ]
    # send_value_to_range_resource(host, token, resources)


def random_string():
    size = random.randint(1, 10)
    data = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for _ in range(size))
    return data


def getData(resource):
    data = random_string()
    print "Data: {}={}".format(resource, data)
    return "{}={}".format(resource, data)


def send_value_to_range_resource(host, token, resources):
    for x in resources:
        print "------------------------"
        print "Resource: {}".format(x)
        data = getData(resource)
        response = post_request(host, token, data)
        print response
        print response.content
        print "------------------------"


def send_value_to_resource(host, token, resource, count):
    for x in xrange(count):
        print "------------------------"
        print "Count: {}".format(x)
        data = getData(resource)
        response = post_request(host, token, data)
        print response
        print response.content
        print "------------------------"


def send_value_to_resource_bizapi(host, projectId, sn, resource, count):
    for x in xrange(count):
        print "------------------------"
        print "Count: {}".format(x)
        data = random_string()
        response = patch_request(host, projectId, sn, {resource: data})
        print response
        print response.content
        print "------------------------"


def patch_request(host, projectId, sn, data):
    HEADER = {'content-type': 'application/json',
              'Authorization': 'Basic dGVzdGluZ0BleG9zaXRlLmNvbToxMjM0ZXN6eGN2Kys='}
    print data
    try:
        response = requests.patch("{host}/service/{projectId}/device2/identity/{sn}/state".format(**locals()),
                                  headers=HEADER,
                                  data=json.dumps(data)
                                  )
    except Exception, e:
        print e
    return response


def post_request(host, token, data):
    HEADER = {'content-type': 'application/x-www-form-urlencoded; charset=utf-8',
              'X-Exosite-CIK': token}
    response = ''
    try:
        response = requests.post(
            "{}/onep:v1/stack/alias".format(host),
            headers=HEADER,
            data=data
        )
    except Exception, e:
        print e
    return response

if __name__ == '__main__':
    main()
