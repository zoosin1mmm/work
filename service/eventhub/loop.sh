#!/bin/bash

COUNT="$1"
if [[ -z "$COUNT" ]]; then
    COUNT=2
fi
for (( c=1; c<=COUNT; c++ ))
  do
    RESP=$(
    curl -X POST 'http://event-hub-dev.hosted.exosite.io/api/v1/eventhub/x54elbta82lc0s4ss/messages' \
    -d '{"solution_id":"x54elbta82lc0s4ss","id":"1","publisher":"123456789","event_data":"{\"hello\":\"eventhubdemo\"}", "config_params":[{"sas_key_name":"key0","sas_key":"O+ZO1+8xJocKwysiozLnKIccq2pkks4wafuOfEZh0wQ=", "namespace":"eventhub-qa-test","id":"1","event_hub":"eventhub-1"}]}' \
    -H 'content-type: application/json' 
    )
    printf $RESP
  done