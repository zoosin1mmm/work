#!/bin/bash

IFS=$'\n'
shopt -s nullglob extglob
set -ex

[[ -n ${EMAIL:="testing@exosite.com"} ]]
[[ -n ${PASSWORD:="1234eszxcv++"} ]]
[[ -n ${API:="staging"} ]]
[[ -n ${BIZID:="zj06hv3w8zen4s4i"} ]]    # qa-adc-testing on dev
[[ -n ${PEGASUSAPI:="http://localhost:8081/api/v1"} ]]

# check pegasus API is ready
CHECK_PEGASUS=$(curl -w %{http_code} -s --output /dev/null $PEGASUSAPI/service)
if [[ ${CHECK_PEGASUS} != "200" ]]; then
    echo "Pegasus API is NOT ready!!\n"
    echo "API url: '${PEGASUSAPI}'"
    exit -1
fi

BIZAPI="https://bizapi-$API.hosted.exosite.io/api:1"
time=$(date +%s)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Get a bizapi auth <token>
[[ -z $TOKEN ]] &&
    TOKEN=$(
        curl -s \
            -X POST \
            "$BIZAPI/token/" \
            -H 'Content-Type: application/json' \
            -d '{"email":"'"$EMAIL"'","password":"'"$PASSWORD"'","ttl":86400}' |
        jq  -r .token
    )

# LABEL="testing-coreservice-${time}-qa"
LABEL="testing-coreservice-1497323639-qa"
PROJECTID=y16qhrmj6hrekg0s4
# Create a new application, and get its applicationId
# if [[ -z "$PROJECTID" ]]; then
#     PROJECTID=$(
#         curl -s \
#             -X POST \
#             "$BIZAPI/business/$BIZID/solution/" \
#             -H 'Content-Type: application/json' \
#             -H "Authorization: token $TOKEN" \
#             -d '{"label":"'${LABEL}'", "type":"application"}' |
#         jq  -r .id
#     )
# fi

echo PROJECTID=$PROJECTID

SERVICE_ALIAS=bikesafer06
API_SERVICE_ALIAS=bikesafer06

echo "Create a service"
SERVICE_ID=$(curl -s $PEGASUSAPI/service \
     -H "Content-Type: application/json" \
    -d '@/home/stacy/test.json') # test file limit
     # -d '{"alias":"'${SERVICE_ALIAS}'","schema":{"swagger":"2.0","info":{"title":"Test api-gurus neowsapp.com","description":"Johnson test create service","version":"v1.1","contact":{"name":"Johnson Chuang","email":"johnsonchuang@exosite.com"}},"basePath":"/","host":"www.neowsapp.com","paths":{"/rest/v1/stats":{"get":{"operationId":"getStats","summary":"GET neowsapp stats","description":"GET neowsapp stats","responses":{"200":{"description":"OK","schema":{"type":"object","description":"Response content"}}}}},"/rest/v1/feed/today":{"get":{"operationId":"getToday","summary":"GET today near_earth_objects feed","description":"GET today near_earth_objects feed","responses":{"200":{"description":"OK","schema":{"type":"object","description":"Response content"}}}}}},"consumes":["application/json"],"produces":["application/json"],"schemes":["http"]}}' | jq  -r .id)

echo $SERVICE_ID

if [[ -z "${SERVICE_ID}" ]]; then
    echo "Create service failed!"
fi

echo "Publish the Service"
curl $PEGASUSAPI/service/$SERVICE_ALIAS -X PUT \
-H "Content-Type: application/json" -d '{"status":"available"}'

# check /health & /logs of the published service

# echo "Create a service configuration (subscribe service)"
# curl $PEGASUSAPI/serviceconfig \
# -H 'Content-Type: application/json' \
# -d '{"service":"'${SERVICE_ALIAS}'","solution_id":"'${PROJECTID}'"}'

# echo "Create endpoint in Solution"
# ENDPOINT_PATH="/testpublicapi"
# ENDPOINT_ID=$(curl -s https://bizapi-$API.hosted.exosite.io/api:1/solution/$PROJECTID/endpoint \
# -H 'Authorization: token '${TOKEN} \
# -d '{"method":"GET","path":"'${ENDPOINT_PATH}'","script":"return '${API_SERVICE_ALIAS}'.getquotes()"}' \
# -H 'Content-Type: application/json' | jq  -r .id)
# if [[ -z "${ENDPOINT_ID}" ]]; then
#     echo "Create Endpoint failed!"
# fi

# echo "Give it couple seconds to create an endpoint"
# sleep 3s

# echo "Call the endpoint"
# ENDPOINT_URL="https://${LABEL}.apps.exosite-${API}.io${ENDPOINT_PATH}"
# ENDPOINT_RESPONSE=$(curl -w %{http_code} -s --output /dev/null ${ENDPOINT_URL})

# if [[ ${ENDPOINT_RESPONSE} != "200" ]]; then
#     echo "Test Endpoint response is not 200. It was '${ENDPOINT_RESPONSE}'!"
# fi

# echo "Delete the service"
# curl -X DELETE "${PEGASUSAPI}/service/${SERVICE_ID}?force=true" -H 'Accept: application/json'

# echo "Delete the solution"
# curl -X DELETE https://bizapi-${API}.hosted.exosite.io/api:1/business/${BIZID}/solution/${PROJECTID} \
# -H 'Authorization: token '${TOKEN} \
# -H 'Accept: application/json'

# echo "double check endpoint is 404"
# D_ENDPOINT_RESPONSE=$(curl -w %{http_code} -s --output /dev/null ${ENDPOINT_URL})

# if [[ ${D_ENDPOINT_RESPONSE} != "404" ]]; then
#     echo "Endpoint should've been deleted. BUT it's '${D_ENDPOINT_RESPONSE}'!"
#     exit -1
# elif [[ ${D_ENDPOINT_RESPONSE} == "404" ]]; then
#     echo "Endpoint is deleted successfully!"
# fi