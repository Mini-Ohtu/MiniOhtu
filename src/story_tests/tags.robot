*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Database

*** Variables ***
${AUTHOR}    Test Author
${TITLE}     Test Title
${YEAR}      2024
${PUBLISHER} Test Publisher

*** Test Cases ***

Test Create New Tag
    Go To  ${HOME_URL}
    Click Link  Create a new tag
    Input Text  tag_name  unread
    Click Submit Button
    Click Link  Back
    Go To  ${HOME_URL}
    Wait Until Page Contains  unread
    Should Contain  ${OUTPUT}    unread


Test Add Book
    Go To  ${HOME_URL}
    Click Link  Create new reference
    Input Text  citekey  book-test-2
    Input Text  author  Test Author
    Input Text  title  Test Title
    Input Text  year  2024
    Input Text  publisher  Test Publisher
    Click Save Button
    Wait Until Page Contains  Reference added
    Should Contain  ${OUTPUT}    Reference added

Test Add New Book
    Add Book    book-test

Test Add Second Book
    Add Book    book-test-2

Test Attach Existing Tag To Reference
    Run Keyword    Test Create New Tag
    Run Keyword    Test Add New Book
    Go To  ${HOME_URL}
    Click Link  Add tags
    Select From List By Label  id_tags  unread
    Click Submit Button
    Go To  ${HOME_URL}
    Wait Until Page Contains  @book{ book-1
    Wait Until Page Contains  tag = { unread }

Tag can be used as filter
    Run Keyword    Test Attach Existing Tag To Reference
    Run Keyword    Test Add Second Book
    Go To  ${HOME_URL}
    Click Link  unread
    Wait Until Page Contains    @book{ book-1
    Wait Until Page Does Not Contain    @book{ book-2


