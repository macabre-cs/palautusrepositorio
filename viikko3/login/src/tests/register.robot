*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application Create User And Go To Register Page

*** Test Cases ***

Register With Valid Username And Password
    Set Username  bambuhai
    Set Password  bambuhai123
    Set Password Confirmation  bambuhai123
    Click Button  Register
    Register Should Succeed

Register With Too Short Username And Valid Password
    Set Username  mi
    Set Password  maumau123
    Set Password Confirmation  maumau123
    Click Button  Register
    Register Should Fail With Message  Username must be at least 3 characters long

Register With Valid Username And Too Short Password
    Set Username  hauki
    Set Password  ha
    Set Password Confirmation  ha
    Click Button  Register
    Register Should Fail With Message  Password must be at least 8 characters long

Register With Valid Username And Invalid Password
    Set Username  ahven
    Set Password  ahvenonkala
    Set Password Confirmation  ahvenonkala
    Click Button  Register
    Register Should Fail With Message  Password cannot contain only letters

Register With Nonmatching Password And Password Confirmation
    Set Username  särki
    Set Password  sarki123
    Set Password Confirmation  sarki456
    Click Button  Register
    Register Should Fail With Message  Password and password confirmation do not match

Register With Username That Is Already In Use
    Set Username  kalle
    Set Password  kalle123
    Set Password Confirmation  kalle123
    Click Button  Register
    Register Should Fail With Message  Username is already taken

*** Keywords ***
Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Password
    [Arguments]  ${password}
    Input Password  password  ${password}

 Set Password Confirmation
    [Arguments]  ${password_confirmation}
    Input Password  password_confirmation  ${password_confirmation}

Register Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Page Should Contain  ${message}

Register Should Succeed
    Welcome Page Should Be Open

*** Keywords ***
Reset Application Create User And Go To Register Page
    Reset Application
    Create User  kalle  kalle123
    Go To Register Page