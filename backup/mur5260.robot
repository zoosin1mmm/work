
Murano CLI can syncup all project
    [Setup]    TestSetupForCreateFileAndSolution
    [Template]    Syncup All Porject And Verify Porject Is Synced
    syncup
    push
    [Teardown]    TestTeardownForDeleteAllDirectory

Murano CLI can syncup application
    [Setup]    TestSetupForCreateFileAndApplication
    [Template]    Syncup Application And Verify Application Is Synced
    syncup    --type    application
    application     push
    push      application
    [Teardown]    TestTeardownForDeleteAllDirectory

Murano CLI can syncup product
    [Setup]    TestSetupForCreateFileAndApplication
    [Template]    Syncup Product And Verify Product Is Synced
    syncup    --type    product
    product     push
    push      product
    [Teardown]    TestTeardownForDeleteAllDirectory

Syncup All Porject And Verify Porject Is Synced
    [Arguments]    ${command}
    Create All Service File
    ${resp} =    Shell Call    murano    ${command}
    Verify Two Specific Parameters From Gateway Info Should Contain Expected    ${applicationID}    resources    ${random}    ${resourceContent}
    Verify Application Should Contain Module    ${applicationID}    ${random}
    Verify Endpoint Is Existing In Application    ${applicationID}    get    /${random}
    Verify Eventhandler Script As Expected    ${applicationID}    user    account    print("${random}")
    [Teardown]    Delete All Service File And Revert Syncup Data

Syncup Application And Verify Application Is Synced
    [Arguments]    ${command}    ${function}    ${option}=${EMPTY}
    Create All Service File
    ${resp} =    Shell Call    murano    ${command}    ${function}    ${option}
    Verify Application Should Contain Module    ${applicationID}    ${random}
    Verify Endpoint Is Existing In Application    ${applicationID}    get    /${random}
    Verify Eventhandler Script As Expected    ${applicationID}    user    account    print("${random}")
    [Teardown]    Delete All Service File And Revert Syncup Data

Verify Two Specific Parameters From Gateway Info Should Not Contain Expected
    [Documentation]    Verify specific data in specific object of the response from gateway setting contain not expected datas
    [Arguments]    ${solutionID}    ${key}    ${subKey}    @{expected}
    ${resp} =    Get Data From Specific Parameters Of Gateway Info    ${solutionID}    ${key}
    ${data} =    Get From Dictionary    ${resp}    ${subKey}
    Verify Response Should Not Contain Expected List    ${resp}    @{expected}


Syncup Product And Verify Product Is Synced
    [Arguments]    ${command}    ${function}    ${option}=${EMPTY}
    Create All Service File
    ${resp} =    Shell Call    murano    ${command}    ${function}    ${option}
    Verify Two Specific Parameters From Gateway Info Should Contain Expected    ${applicationID}    resources    ${random}    ${resourceContent}
    [Teardown]    Delete All Service File And Revert Syncup Data

Verify Eventhandler Script As Expected
    [Documentation]    Verify serviceconfig script is match
    [Arguments]    ${applicationID}    ${service}    ${event}    ${script}
    ${script} =    Replace String    "    \"
    ${serviceconfig} =    Get Eventhandler Detail Via API    ${applicationID}    ${service}    ${event}
    Verify Object Key Value As Expected    ${resp}    script    ${script}

Delete All Service File And Revert Syncup Data
    Remove Files    ${modulesDir}${/}resources.yaml    ${resourceDir}${/}${random}.lua    ${routesDir}${/}${random}.get.lua    ${servicesDir}${/}{product.id}_event.lua
    ${resp} =    Shell Call    murano    syncup    --delete

Verify Endpoint Is Existing In Application
    [Documentation]    Verify specific endpoint is existing in application
    [Arguments]    ${solutionID}    ${method}    ${path}
    ${resp} =    Solution SolutionID Endpoint Get    ${solutionID}
    ${path} =    Catenate    SEPARATOR=    /    ${path}
    ${endpoint} =    Evaluate    filter(lambda i: re.search('${path}', i['path']) and re.search('${method}', i['method']), ${resp.json()})    re

Verify Application Should Contain Module
    [Arguments]    ${applicationID}    ${moduleName}
    ${list}    ${total} =    Get Module List    ${applicationID}
    Verify Result Should Contain Expected Message    ${list}    u'name': u'${moduleName}'

TestTeardownForDeleteAllDirectory
    Remove Directory    ${modulesDir}    recursive=True
    Remove Directory    ${resourceDir}    recursive=True
    Remove Directory    ${routesDir}    recursive=True
    Remove Directory    ${servicesDir}    recursive=True

Create All Service Directory
    Set Test Variable    ${modulesDir}    ${fileDir}/modules
    Set Test Variable    ${routesDir}    ${fileDir}/routes
    Set Test Variable    ${servicesDir}    ${fileDir}/services
    Set Test Variable    ${resourceDir}    ${fileDir}/specs
    Create Directory    ${modulesDir}
    Create Directory    ${resourceDir}
    Create Directory    ${routesDir}
    Create Directory    ${servicesDir}
    Create Application And Product

TestSetupForCreateFileAndSolution
    Create All Service Directory
    TestSetupForCreateAndSetSolution

TestSetupForCreateFileAndApplication
    Create All Service Directory
    ${time} =    Evaluate    time.strftime("%Y%m%d%H%M%S")    time
    Set Test Variable    ${applicationName}    testing-${time}-qa
    Set Test Variable    ${domain}    https://${applicationName}.${SOLUTION_HOST}
    ${applicationID} =    Create Solution Via API    ${applicationName}    businessId=${VALID_ADC_COMPANY_ID}    types=application
    Set Test Variable    ${applicationID}
    Shell Call    murano    config    application.id    ${applicationID}

Create All Service File
    ${random} =    Generate Random String    5    [LETTERS]
    ${resource} =    catenate  SEPARATOR=\n
    ...    ---\n
    ...        ${random}:\n
    ...          allowed: []\n
    ...          format: string\n
    ...          settable: false\n
    ...          unit: ''
    ${scripts} =    print("${random}")
    ${resourceContent} =    To Json    {"format":"string","settable":false,"unit":"","allowed":[]}
    Create Specified Data File    resources.yaml    ${fileDir}/specs    ${resource}
    Create Specified Data File    ${random}.lua    ${fileDir}/modules    ${scripts}
    Create Specified Data File    ${random}.get.lua    ${fileDir}/routes    ${scripts}
    Create Specified Data File    user_account.lua    ${fileDir}/services    ${scripts}
    Set Test Variable    ${random}
    Set Test Variable    ${resourceContent}
