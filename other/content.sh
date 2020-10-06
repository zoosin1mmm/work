#!/bin/bash

IFS=$'\n'
shopt -s nullglob extglob
set -ex

[[ -n ${CONTENT=${BASH_SOURCE[0]}} ]]
[[ -n ${CONTENT_NAME:=${CONTENT##*/}} ]]
[[ -n ${CONTENT_TYPE:=$(file --brief --mime-type "${CONTENT}")} ]]

# Delete if already exists
#curl -i -X DELETE "http://127.0.0.1:5000/delete/dqa?name=${CONTENT_NAME}"

# Get the S3 POST instructions JSON
[[ -z $UPLOAD ]] &&
    UPLOAD=$(
        curl -s -XPOST -d '{"id":"testing-qa-04247"}' -H 'Content-Type:application/json'\
            "https://content-test.apps.exosite-staging.io/content/upload" |
        jq -c .
    )

jq -r <<<"$UPLOAD" .
#CONTENT_ID=$(jq -r <<<"$UPLOAD" '.id')
UPLOAD_METHOD=$(jq -r <<<"$UPLOAD" '.method')
UPLOAD_URL=$(jq -r <<<"$UPLOAD" '.url')
UPLOAD_ENCTYPE=$(jq -r <<<"$UPLOAD" '.enctype')
# Generate array of -Fkey=value -Fkey=value
UPLOAD_INPUTS=($(jq -r <<<"$UPLOAD" '.inputs | to_entries[] | "-F " + .key + "=" + .value'))
UPLOAD_FIELD=$(jq -r <<<"$UPLOAD" '.field')


echo "curl -i -X '$UPLOAD_METHOD' '$UPLOAD_URL' -H 'Content-Type: $UPLOAD_ENCTYPE' ${UPLOAD_INPUTS[@]} -F '$UPLOAD_FIELD=@$CONTENT'"

# Upload the file
#curl -i \
#    -X "$UPLOAD_METHOD" \
#    "$UPLOAD_URL" \
#    -H "Content-Type: $UPLOAD_ENCTYPE" \
#    "${UPLOAD_INPUTS[@]}" \
#    -F "$UPLOAD_FIELD=@$CONTENT"
#
# Get the S3 GET instructions JSON
#[[ -z $DOWNLOAD ]] &&
#    DOWNLOAD=$(
#        curl -s \
#            "http://127.0.0.1:5000/download/dqa?expires_in=3600&name=${CONTENT_NAME}" \
#            -H "Authorization: token $TOKEN" |
#        jq -c .
#    )

#DOWNLOAD_URL=$(jq -r <<<"$DOWNLOAD" '.url')

# Verify the file exists
#curl -si "$DOWNLOAD_URL" | sed -n '1,/^[^A-Za-z]/p'
