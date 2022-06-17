*** Settings ***
Documentation       BGP test case
Library             ../NetworkTests.py
Suite Setup         Initial Config
Suite Teardown      Final Config

*** Variables ***
${BGP_STATE}             Established

*** Keywords ***
Initial Config
    Connect To All Devices
    Apply Initial Config
    Sleep    20s

Final Config
    Apply Final Config
    Disconnect From All Devices

*** Test Cases ***
Initial BGP Status
    ${state}=    Check Bgp State
    Should Be Equal As Strings      ${state}      ${BGP_STATE}

Incorrect BGP Authentication
    Apply Problem State
    Sleep     5s
    ${state}=    Check Bgp State
    Should Not Be Equal As Strings      ${state}      ${BGP_STATE}


