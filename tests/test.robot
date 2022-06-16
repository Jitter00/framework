*** Settings ***
Documentation       Sample framework for network testing
Library             ../JunosDevice.py
Suite Setup         Initial Config
Suite Teardown      Final Config

*** Variables ***
&{HOST 1}                ip=vsrx1
&{HOST 2}                ip=vsrx2
@{HOSTS}                 &{HOST 1}    &{HOST 2}
${USERNAME}              cristian
${PASSWORD}              Juniper
${BGP_STATE}             Established

*** Keywords ***
Initial Config
    FOR    ${HOST}    IN   @{HOSTS}
        Connect Device  host=${HOST.ip}     username=${USERNAME}     password=${PASSWORD}
        Apply Config    cfg=${HOST.ip}_initial      from_file=True
    END
    Sleep   15s

Final Config
    FOR    ${HOST}    IN   @{HOSTS}
        Connect Device  host=${HOST.ip}     username=${USERNAME}     password=${PASSWORD}
        Apply Config    cfg=${HOST.ip}_final      from_file=True
    END

*** Test Cases ***
Initial BGP Status
    FOR    ${HOST}    IN   @{HOSTS}
        Connect Device  host=${HOST.ip}     username=${USERNAME}     password=${PASSWORD}
        ${state}=    Check Bgp State
        Should Be Equal As Strings      ${state}      ${BGP_STATE}
    END

Wrong BGP Authentication
    Connect Device  host=vsrx1     username=${USERNAME}     password=${PASSWORD}
    Apply Config    cfg=wrong_key      from_file=True
    Sleep   5s
    ${state}=    Check Bgp State
    Should Not Be Equal As Strings      ${state}      ${BGP_STATE}
