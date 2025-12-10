*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Database

*** Test Cases ***

Generated citekey uses significant title word
    Go To  ${HOME_URL}
    Click Link  Create new reference
    Wait Until Element Is Visible  id:author
    Input Text  author  Jane Doe
    Input Text  title  The Analysis of Big Data
    Input Text  year  2024
    Input Text  publisher  Test Publisher
    Wait Until Element Is Visible  id:generate-citekey-btn
    Click Button  id:generate-citekey-btn
    Wait Until Keyword Succeeds  5x  1 second  Citekey Should Match Pattern  Doe2024(Analysis|Big|Data)

*** Keywords ***
Citekey Should Match Pattern
    [Arguments]  ${pattern}
    ${value}=  Get Value  id:citekey
    Should Match Regexp  ${value}  ${pattern}
