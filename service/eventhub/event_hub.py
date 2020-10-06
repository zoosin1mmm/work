import time
import urllib
import hmac
import hashlib
import base64
import requests
import json

def get_auth_token(sb_name, eh_name, sas_name, sas_value):
    """
    Returns an authorization token dictionary 
    for making calls to Event Hubs REST API.
    """
    host = "{}.servicebus.windows.net".format(sb_name)
    uri = urllib.quote_plus("https://{}/{}".format(host, eh_name))
    sas = sas_value.encode('utf-8')
    expiry = str(int(time.time() + 10000))
    string_to_sign = (uri + '\n' + expiry).encode('utf-8')
    signed_hmac_sha256 = hmac.HMAC(sas, string_to_sign, hashlib.sha256)
    signature =urllib.quote_plus(base64.b64encode(signed_hmac_sha256.digest()))
    token = 'SharedAccessSignature sr={}&sig={}&se={}&skn={}'.format(uri, signature, expiry, sas_name)
    HEADER = {'content-type': 'application/atom+xml;type=entry;charset=utf-8',
              'Host': host,
              'Authorization':token}
    data = { "Location": "Redmond", "Temperature":"37.0" }
    try:
        response = requests.post(
            'https://{}/{}/publishers/test/messages'.format(host, eh_name),
            json=data,
            headers=HEADER
        )
        print(response)
    except Exception, e:
        print "Connect Error: {}".format(e)
    print("--------------------------------------------")
    print("curl -X POST -ik \\")
    print("https://eventhub-qa-test.servicebus.windows.net/eventhub-1/publishers/test/messages \\")
    print("-d '"+str(data)+"  ' \\")
    print("-H 'Authorization : "+token+"' \\")
    print("-H 'Content-Type: application/atom+xml;type=entry;charset=utf-8 ' \\")
    print("-H 'Host: "+host+"'")
    print("--------------------------------------------")

if __name__ == '__main__':
    get_auth_token("eventhub-qa-test","eventhub-1","RootManageSharedAccessKey","Tu7dnyJnzWjotQ18YzWYd5V0mFU+Y+kpCYNvu+fwJxo=")
