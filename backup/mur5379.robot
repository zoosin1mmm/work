Murano CLI can syncdown all project
    [Setup]    Create And Set Solution
    [Template]    Create Service And Syncdown All Projcet
    syncdown
    pull
    [Teardown]    TestTeardownForDeleteSolution

Murano CLI can syncdown application
    [Setup]    Create And Set Solution
    [Template]    Create Service And Syncdown Application
    syncdown    --type    application
    application    pull
    pull    application
    [Teardown]    TestTeardownForDeleteSolution

Murano CLI can syncdown product
    [Setup]    Create And Set Solution
    [Template]    Create Service And Syncdown Product
    syncdown    --type    product
    product    pull
    pull    product
    [Teardown]    TestTeardownForDeleteSolution

Create Service And Syncdown All Projcet
    [Arguments]    ${command}
    Create Service To Product And Application
    ${resp} =    Shell Call    murano    ${command}
    Verify Sync Data Should Contain As Expected    ${modulesDir}/${random}.lua    return "${random}"
    Verify Sync Data Should Contain As Expected    ${routerDir}/${random}.get.lua    return "${random}"
    Verify Sync Data Should Contain As Expected    ${servicesDir}/timer_timer.lua    print("${random}")
    Verify Sync Data Should Contain As Expected    ${resourceDir}/resources.yaml    ${random}
    [Teardown]    TestTeardownForDeleteAllDirectory

Create Service And Syncdown Application
    [Arguments]    ${command}    ${function}    ${option}=${EMPTY}
    Create Service To Product And Application
    ${resp} =    Shell Call    murano    ${command}    ${function}    ${option}
    Verify Sync Data Should Contain As Expected    ${modulesDir}/${random}.lua    return "${random}"
    Verify Sync Data Should Contain As Expected    ${routerDir}/${random}.get.lua    return "${random}"
    Verify Sync Data Should Contain As Expected    ${servicesDir}/timer_timer.lua    print("${random}")
    Verify Sync Data Should Not Contain As Expected    ${resourceDir}/resources.yaml    ${random}
    [Teardown]    TestTeardownForDeleteAllDirectory

Create Service And Syncdown Product
    [Arguments]    ${command}    ${function}    ${option}=${EMPTY}
    Create Service To Product And Application
    ${resp} =    Shell Call    murano    ${command}    ${function}    ${option}
    Verify File Is Not Existing    ${modulesDir}/${random}.lua
    Verify File Is Not Existing    ${routerDir}/${random}.get.lua
    Verify File Is Not Existing    ${servicesDir}/timer_timer.lua
    Verify Sync Data Should Contain As Expected    ${resourceDir}/resources.yaml    ${random}
    [Teardown]    TestTeardownForDeleteAllDirectory

Verify Sync Data Should Contain As Expected
    [Documentation]    Verify local file is existing and content is correct
    [Arguments]    ${path}    ${dataContent}
    ${data} =    Get File    ${path}
    ${data} =    Split String    ${data}    \n
    ${data} =    Evaluate    json.dumps('''${data}''')    json
    Verify Result Should Contain Expected Message    ${data}    ${dataContent}

Verify File Is Not Existing
    [Documentation]    Verify file is not existing
    [Arguments]    ${path}
    ${status}    ${data} =    Run Keyword And Ignore Error    Get File    ${path}
    Should Be Equal    ${status}    FAIL

Verify Sync Data Should Not Contain As Expected
    [Documentation]    Verify file data should not contain specific data
    [Arguments]    ${path}    ${dataContent}
    ${data} =    Get File    ${path}
    ${data} =    Split String    ${data}    \n
    ${data} =    Convert To String    ${data}
    ${dataContent} =    Convert To String    ${dataContent}
    Verify Result Should Not Contain Expected Message    ${data}    ${dataContent}

Create Service To Product And Application
    ${random} =    Generate Random String    5    [LETTERS]
    Create Endpoint Via API    ${applicationID}    GET    ${random}    return "${random}"
    Create Module Via API    ${applicationID}    ${random}    return "${random}"
    Create Resource Via Adc API    ${productID}    {"resources":{"${random}":{"format":"string","settable":false}}}
    Update Service Timer    ${applicationID}    print("${random}")
    Set Test Variable    ${modulesDir}    ${fileDir}/modules
    Set Test Variable    ${random}
    Set Test Variable    ${resourceDir}    ${fileDir}/specs
    Set Test Variable    ${routerDir}    ${fileDir}/routes
    Set Test Variable    ${servicesDir}    ${fileDir}/services