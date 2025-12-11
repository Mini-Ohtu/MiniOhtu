*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Database


*** Test Cases ***

Copy all the things in the page
    Go To  ${HOME_URL}/populate
    Go To  ${HOME_URL}
    Click Button  Copy all
    



Copy just the searched things
    Go To  ${HOME_URL}/populate


Copy singular thing
    Go To  ${HOME_URL}/populate

