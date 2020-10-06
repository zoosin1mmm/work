${database}    db1fcef5f64f58eee36a09a60d95c25ced
${hostname}    murano-rds-staging-databases.csbg0yn8ehcm.us-west-1.rds.amazonaws.com
${password}    Kg6yWLTepWp68VDuCw2itaRBduishDjRRMUw
${username}    db1fcef5f64f58eee36a09a60d95c25ced

Murano CLI can postgresql with sql
    [Setup]    TestSetupForCreateApplicationAndTable
    ${result} =    Shell Call    murano    postgresql    ${selectSQL}
    Verify Response Content Should Contain Message    ${result}    {"data":"data"}
    [Teardown]    Delete Solution Via API    ${applicationName}    businessId=${VALID_ADC_COMPANY_ID}

Murano CLI can get application logs
	[Setup]    TestSetupForCreateApplicationAndTriggerLog
	[Template]    Trigger Application Log And Verify Log Content
	logs
	logs    application
    application    logs
    [Teardown]    Delete Solution Via API    ${applicationName}    businessId=${VALID_ADC_COMPANY_ID}

Trigger Application Log And Verify Log Content
	[Arguments]    ${command}    ${function}=${EMPTY}
	${result} =    Shell Call    murano    ${command}    ${function}    --raw
    Verify Result Line Should Contain Expected Message    ${result}    type=>"script"    message=>"Endpoint POST /muranocli/timer done with code=200"
    Verify Result Line Should Contain Expected Message    ${result}    type=>"call"    message=>"service call failed"
    Verify Result Line Should Contain Expected Message    ${result}    type=>"event"    message=>"script failed"
    Verify Result Line Should Contain Expected Message    ${result}    type=>"config"    message=>"Solution created library."
    Verify Result Line Should Contain Expected Message    ${result}    type=>"service"

Create Application And Upload Router
    ${time} =    Evaluate    time.strftime("%Y%m%d%H%M%S")    time
    Set Test Variable    ${applicationName}    testing-${time}-qa
    Set Test Variable    ${domain}    https://${applicationName}.${SOLUTION_HOST}
    ${applicationID} =    Create Solution Via API    ${applicationName}    businessId=${VALID_ADC_COMPANY_ID}    types=application
    Upload Route File From Resource Dictionary    ${applicationID}    service_muranocli
    Add Service To Solution    ${applicationID}    postgresql
    Update Serviceconfig Via API    ${solutionID}    postgresql    {"parameters":{"Username":"${username}","Password":"${password}","Hostname":"${hostname}","Database":"${database}"}}
    Create Session    solution    ${domain}    verify=False

TestSetupForCreateApplicationAndTable
    Create Application And Upload Router
    ${time} =    Evaluate    time.strftime("%Y%m%d%H%M%S")   time
    ${column} =    Generate Random String    5    [LOWER]
    ${value} =    Generate Random String    5    [LOWER]
    &{data} =    Create Dictionary    createSQL=CREATE TABLE qa${time} (${column} varchar)    insertSQL=INSERT INTO qa${time} VALUES ($${value}$);
    ${resp} =    Post Request    solution    /muranocli/relationalDB/insert    data=&{data}    headers=&{headers}
    Set Test Variable    ${selectSQL}    SELECT * FROM qa${time}

TestSetupForCreateApplicationAndTriggerLog
	Create Application And Upload Router
    Trigger Log Of All Type

Trigger Log Of All Type
	${random} =    Generate Random String    5    [LETTERS]
	Update Eventhandler Via API    ${applicationID}    timer    timer    print(request)
    ${resp} =    Post Request    solution    /muranocli/timer    data={"timer_id":"${random}", "message":"${random}", "duration":1000}    headers=&{headers}
	${resp} =    Post Request    solution    /muranocli/timer    data={}    headers=&{headers}
	Create Module Via API    ${applicationID}   ${random}
	Set Test Variable    ${random}

Verify Result Line Should Contain Expected Message
    [Documentation]    Verify result line should contain expected string
    [Arguments]    ${line}    ${expectedLine}    @{expected}
    ${result} =    Split String    ${line}    \n
    ${line} =    Evaluate    filter((lambda x: re.search('${data}', x['data'])), ${result})    re
    Verify Result Should Contain As Multiple Expected    ${line[0]}    @{expected}

