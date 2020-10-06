#!/bin/bash
# IFS=$'\n'
# shopt -s nullglob extglob
# set -ex

# solutionID='vhnd0daxg2b7qfr'
# timestamp=$(date +%s)
host="stacychen.apps.exosite-dev.io"
solutionName="stacychen"
businessID="r4q2m9xs2w"
solutionID="k23s6ncubxmm80000"
TOKEN="Basic dGVzdGluZ0BleG9zaXRlLmNvbToxMjM0ZXN6eGN2Kys= "
alias="testingservice"
title="$alias-testing"

# [[ -z $solutionID ]] &&
#     solutionID=$(curl "http://localhost:8081/api/v1/solution" \
#     -X POST  -H 'content-type: application/json' \
#     --data-binary '{"label": "'$solutionName'", "type": "application"}')

elementId=$(curl -X POST \
  https://bizapi-staging.hosted.exosite.io/api:1/exchange/r4q2m9xs2w/element/ \
  -H 'authorization: Basic dGVzdGluZ0BleG9zaXRlLmNvbToxMjM0ZXN6eGN2Kys=' \
  -H 'content-type: application/json' \
  -d '{
"bizid": "r4q2m9xs2w",
"type":"service",
"name":"testingservice",
"description": "Configure a Murano solution to make calls and send SMS notifications",
"source": {
        "from": "service",
        "name": "testingservice",
        "schema": " \n swagger: '2.0' \n info: \n   version: v1 \n   title: Testing \n   description: Testing \n   contact: \n     name: Testing \n     email: testing@exosite.com \n schemes: \n - https \n host: stacychen.apps.exosite-dev.io \n x-healthPath: '/' \n basePath: '/' \n x-config-parameters: \n - name: private \n   description: A private parameter \n   x-internal-use: true \n   type: string \n paths: \n   '/qa': \n     get: \n       description: A testing operation \n       operationId: get \n       parameters: [] \n       responses: \n         default:\n           description: Return the operation result \n x-events: \n   event: \n     type: SQS \n     summary: Test service \n     description: Test service \n     parameters: \n     - name: qa \n       in: body \n       schema: \n         type: string \n         description: Return eventhandler event value"
    },"tags": [
        "testQA"
    ],
    "attachment": {},
    "contact": "QA",
    "specs": "asf",
    "image": {
    }
}')
sleep 1s
echo $elementId

# curl -X POST 'https://bizapi-dev.hosted.exosite.io/api:1/exchange/'$businessID'/purchase/'
# -H "authorization:"$TOKEN"" \
# -H 'Content-Type: application/json' \
# -d '{"elementId": "'$elementId'"}'
curl -X POST \
  'https://bizapi-dev.hosted.exosite.io/api:1/solution/'$solutionID'/serviceconfig' \
  -H 'authorization: Basic dGVzdGluZ0BleG9zaXRlLmNvbToxMjM0ZXN6eGN2Kys=' \
  -H 'content-type: application/json' \
  -d '{"solution_id":"k23s6ncubxmm80000","service":"testingservice"}'

result=(curl -X GET "https://"$host"/test")

echo $result

curl -X DELETE 'https://bizapi-dev.hosted.exosite.io/api:1/exchange/'$businessID'/purchase/'
  -H 'authorization: Basic dGVzdGluZ0BleG9zaXRlLmNvbToxMjM0ZXN6eGN2Kys=' \
-H 'Content-Type: application/json' \
-d '{"elementId": "'$elementId'"}'

# curl "http://localhost:8081/api/v1/eventhandler" \
#     -X POST  -H 'content-type: application/json' \
#     --data-binary '{"service":"'$alias'", "event":"event", "solution_id":"'$solutionID'" }'

# oc port-forward okami-test-h 27017:27017
# curl "http://localhost:4100/api/v1/trigger/$solutionID/$alias/event" -X POST -i