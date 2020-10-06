#!/bin/bash

SOLUTION_ID="$2"
BUSINESS_ID="$3"
EXCHANGE="$1"
if [[ -z "$SOLUTION_ID" ]]; then
    SOLUTION_ID="a27fp8y8qvukg0000"
fi
if [[ -z "$BUSINESS_ID" ]]; then
    BUSINESS_ID="6fd6oo3zryynwmi"
fi
if [[ -z "$EXCHANGE" ]]; then
    EXCHANGE="Y"
fi

TOKEN=$(
      curl 'https://bizapi-staging.hosted.exosite.io/api:1/token/' \
            -H 'content-type: application/json' \
            -X POST -d '{"email": "testing@exosite.com", "password": "1234eszxcv++"}' | jq -r '.token'
)
printf  "solutionID:${SOLUTION_ID} \n"
printf  "BUSINESS_ID:${BUSINESS_ID} \n"
printf  "EXCHANGE:${EXCHANGE} \n"

SERVICE=("timer" "twilio" "auth0" "mbed" "bulknotify" "spms" "http" "salesforceiot" "postgresql" "eventhub" "portals" "scripts" "analytics")
ELEMENTID=("5955b9eeb3e6b2000147cfc0" "5955b9efbf83ba00015fff45" "5955b9ecbf83ba00015fff3f" "59fc07e5a28459000146da6d" "59b6eb1ef50b8f0001dbfcc4" "5955b9edbf83ba00015fff43" "5a040251f0d1e8000102c3d5" "59facfb35e444400016a68f9" "5a2f8d12f2266c000111dee2" "5a435166b9bb180001bf78ed")

Fail=0
count=0

if [[ "$EXCHANGE" == "Y" ]] || [[ "$EXCHANGE" == "y" ]]; then
    printf "Purchase Start"
    for e in "${ELEMENTID[@]}"
    do
        printf "\n--------\n"
        printf "Purchase Element_ID: '$e' \n"
        printf "Purchase Element: ${SERVICE[count]} \n"
        RESP=$(
            curl 'https://bizapi-staging.hosted.exosite.io/api:1/exchange/'$BUSINESS_ID'/purchase/' \
                -H 'content-type: application/json' \
                -H 'Authorization: token '$TOKEN'' \
                -X POST -d '{"elementId":"'$e'"}' | jq -r '.message'
        )

        if [[ "$RESP" == null ]] ; then
            printf "200 Purchase Element Success ..... \n"
        elif [[ "$RESP" == 'elementId '$e' already purchased' ]] ; then
            printf "409 Purchase Element Fail : Conflict Purchase \n"
        elif [[ "$RESP" == 'upgrade' ]] ; then
                printf "409 Purchase Element Fail : Permissions Decline , Please Upgrade Business \n"
                Fail=1
                break  
        elif [[ "$RESP" == 'Insufficient scope' ]] ; then
                printf "403 Not Found \n"
                Fail=1
                break    
        else
            printf "Not Expected Error : $RESP \n"
            Fail=1
            break
        fi
        printf "\n--------\n"
        count=$((++count))
    done
    printf "\n--------\n"
    printf "Purchase End\n"
fi

if [[ "$Fail" == 0 ]]; then
    printf "Service Adding Start\n"
    for i in "${SERVICE[@]}"
    do
        printf "\n--------\n"
        printf "Add Service: $i \n"
        RESP=$(
            curl 'http://localhost:8081/api/v1/solution/'$SOLUTION_ID'/serviceconfig' \
                 -H 'Content-Type: application/json' \
                 -X POST -d '{"service":"'$i'","solution_id":"'$SOLUTION_ID'"}' \
                 -k --silent -L -w "\n%{http_code}"
        )

        STATUS="${RESP##*$'\n'}"           
        CONTENT="${RESP%$'\n'*}"

        if [[ "$STATUS" == 200 ]] ; then
            printf "200 Add Service Success ..... \n"
        elif [[ "$STATUS" == 409 ]] ; then
            printf "409 Add Service Fail : Service Is Existing In Application \n"
        elif [[ "$STATUS" == 424 ]] ; then
            printf "424 Add Service Fail : Service Name InCorrect \n"
            break
        elif [[ "$STATUS" == 000 ]] ; then
            printf "Please login dqa-env/exo-openshift-hopper \n"
            break
        else
            printf "Not Expected Error : ${STATUS} ${CONTENT} \n"
            break
        fi
        printf "\n--------\n"
    done
    printf "\n--------\n"
    printf "Service Adding End\n"
fi

printf "\n -----------End----------\n"

