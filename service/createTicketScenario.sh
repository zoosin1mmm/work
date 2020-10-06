# set -ex
function call_the_route {
    endpoint=$1
    body=$2
    echo "{code}"    
    echo 'curl https://'${application_domain}'/'${endpoint}' \
        -H "content-type: application/json" \
        -d '${body}' -i'
    echo "{code}"
    echo "* return {code}"
    curl https://${application_domain}/${endpoint} \
        -H "content-type: application/json" \
        -d "${body}"
    echo "{code}"
}

# application_domain="teststacy.apps.exosite-staging.io"
application_domain="mur6094.apps.exosite-staging.io"
scenario=('test1')
endpoint=(
    'timer' '\'
)
bodys=(
    '{"duration":100,"message":"testing"}' '\'
    )

next=0

for i in "${scenario[@]}"; do
    echo "{panel:title=Scenario: $i}"
    for (( j = ${next}; j < ${#endpoint[@]}; j++ )); do
        if [[ ${endpoint[j]} == '\' ]]; then
            next=$((++j))
            break
        fi
        echo "* POST with body"
        call_the_route ${endpoint[j]} ${bodys[j]}
    done
    echo "{panel}"
done
