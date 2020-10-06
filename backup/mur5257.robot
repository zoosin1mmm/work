Murano CLI can activate a device
    [Setup]    Create And Set Product
    [Template]    Device Activate And Verify Device Is Existing
    device    activate
    product    device    activate
    [Teardown]    Delete Solution Via API    ${productName}    businessId=${VALID_ADC_COMPANY_ID}

Murano CLI can enable a device with specific type
    [Setup]    TestSetupForCreateProductAndSetAuth
    [Template]    Device Enable With Specific Type
    :FOR    ${type}    IN    @{types}
    \    ${type}    device    enable    ${deviceSN}    --auth=${type}    --cred=${token}
    \    ${type}    product    device    enable    ${deviceSN}    --auth=${type}    --cred=${token}
    certificate    device    enable    ${deviceSN}    --key=${authCret}
    certificate    product    device    enable    ${deviceSN}    --key=${authCret}
    [Teardown]    Delete Solution Via API    ${productName}    businessId=${VALID_ADC_COMPANY_ID}

Murano CLI can write to set of aliases on devices if cloud modifiable
    [Setup]    TestSetupForCreateDeviceAndResource
    [Template]    Write Device Value And Verify Value
    device    write
    product    device    write
    [Teardown]    Delete Solution Via API    ${productName}    businessId=${VALID_ADC_COMPANY_ID}

Murano CLI can read device in 3 seconds
    [Setup]    TestSetupForCreateDeviceAndResource
    [Template]    Write And Read Device Value
    device    read
    product    device    read
    product    device    twee
    [Teardown]    Delete Solution Via API    ${productName}    businessId=${VALID_ADC_COMPANY_ID}

Write And Read Device Value
    [Arguments]    ${command}    ${function}    ${option}=${EMPTY}
    ${value} =    Evaluate    str(random.randint(1, 100))    random
    ${resp} =    Shell Call    murano    device    write    ${deviceSN}    ${resource}=${value}
    ${stdout}    ${time} =    Shell Call    time    -p    murano    ${command}    ${function}    ${option}    ${deviceSN}
    Verify Result Should Contain Expected Message    ${stdout}    | Alias | Reported | Set | Timestamp
    Verify Result Should Contain Expected Message    ${stdout}    ${resource}
    Verify Result Should Contain Expected Message    ${stdout}    ${value}
    Verify Real Time Is Less Than Expected    ${time}    3

Write Device Value And Verify Value
    [Arguments]    ${command}    ${function}    ${option}=${EMPTY}
    ${value} =    Evaluate    str(random.randint(1, 100))    random
    ${resp} =    Shell Call    murano    ${command}    ${function}    ${option}    ${deviceSN}    ${resource}=${value}
    Verify Device State Contain Expected Message    ${deviceSN}    ${resource}
    Verify Device State Contain Expected Message    ${deviceSN}    ${value}
    Verify Device State Is Set As Expected    ${productID}    ${deviceSN}    ${resource}    ${value}
    [Teardown]    Delete Device Via API    ${productID}    ${deviceSN}

TestSetupForCreateProductAndSetAuth
    Create And Set Product
    @{types} =   Create List    token   hash   signature
    ${token} =    Generate Random String    40    [LETTERS]
    ${authCret}    ${cret}    ${cretPem} =    Create TLS Certificate    ${deviceSN}    ${fileDir}/${deviceSN}
    Set Test Variable    ${types}
    Set Test Variable    ${token}

Device Enable With Specific Type
    [Arguments]    ${type}    @{command}
    @{base} =    Create List    time    -p    murano
    @{command} =    Combine Lists    ${base}    ${command}
    ${stdout}    ${time} =    Shell Call    @{command}
    Verify Device List Contain Expected Device    ${deviceSN}
    Verify Device Info Should Be Expected    ${deviceSN}    status    provisioned    ${productID}
    Verify Device Info Should Be Expected    ${deviceSN}    auth    {"type":"${type}"}    ${productID}
    Verify Real Time Is Less Than Expected    ${time}    3
    [Teardown]    Delete Device Via API    ${productID}    ${deviceSN}

Device Activate And Verify Device Is Existing
    [Arguments]    ${command}    ${function}    ${option}=${EMPTY}
    ${stdout}    ${time} =    Shell Call    murano    ${command}    ${function}    ${option}    ${deviceSN}
    Verify Device List Contain Expected Device    ${deviceSN}
    Verify Device Info Should Be Expected    ${deviceSN}    status    provisioned    ${productID}
    Verify Device Info Should Be Expected    ${deviceSN}    auth    {"type":"token"}    ${productID}
    [Teardown]    Delete Device Via API    ${productID}    ${deviceSN}

Verify Device Info Should Be Expected
    [Documentation]    Verify device info with specified key should be expected
    [Arguments]    ${sn}    ${keys}    ${expected}    ${PID}=${PID}
    ${resp} =    Get Device Info Via Adc API    ${PID}    ${sn}
    Verify Response Message As Expected    ${resp.json()${keys}}    ${expected}

