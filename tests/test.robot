*** Settings ***
Documentation       Sample framework for network testing

Library    ../JunosDevice.py

*** Variables ***
&{HOST 1}                ip=vsrx1
&{HOST 2}                ip=vsrx2
@{HOSTS}                 &{HOST 1}    &{HOST 2}
${USERNAME}              cristian
${PASSWORD}              Juniper
${BGP_STATE}             Established

*** Test Cases ***
Check BGP Status
    FOR    ${HOST}    IN   @{HOSTS}
        Connect Device  host=${HOST.ip}     username=${USERNAME}     password=${PASSWORD}
        ${state}=    Check Bgp State
        Should Be Equal As Strings      ${state}      ${BGP_STATE}
    END
