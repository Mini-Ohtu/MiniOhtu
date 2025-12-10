*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Database

*** Variables ***
${AUTHOR}    Test Author
${TITLE}     Test Title
${YEAR}      2024
${PUBLISHER}     Test Publisher
${TAG_NAME_TO_SELECT}    unread

*** Test Cases ***
Empty tag list is shown when no tags added
    Go To  ${HOME_URL}
    Page Should Contain  No tags

After creating a tag it shows up
    Go To  ${HOME_URL}
    Click Button  Create a new tag
    Input Text  tag_name  unread
    Click Save Button
    Wait Until Page Contains  unread
    Go To  ${HOME_URL}
    Wait Until Page Contains  unread
    Page Should Contain  unread

Adding tag to reference when no tags added shows empty tag list
    Go To  ${HOME_URL}
    Click Link  Create new reference
    Input Text  citekey  book-test-2
    Input Text  author  Test Author
    Input Text  title  Test Title
    Input Text  year  2024
    Input Text  publisher  Test Publisher
    Click Save Button
    Wait Until Page Contains  Reference added
    Go To  ${HOME_URL}
    Page Should Contain  book-test-2
    Click Button  Add tags
    Wait Until Page Contains  book-test-2
    Page Should Contain  No tags to add

Clicking tag does not show references before adding
    Go To  ${HOME_URL}
    Click Button  Create a new tag
    Input Text  tag_name  unread
    Click Save Button
    Wait Until Page Contains  unread
    Go To  ${HOME_URL}
    Wait Until Page Contains  unread
    Go To  ${HOME_URL}
    Click Link  unread
    Page Should Contain  No references
