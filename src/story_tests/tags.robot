*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Database

*** Test Cases ***

Tag can be saved to reference
    Go To  ${HOME_URL}
    Click Link  Create new reference
    Input Text  citekey  book-1
    Input Text  author  Article Author
    Input Text  title  Article Title
    Input Text  year  2023
    Input Text  publisher  Book Publisher
    Wait Until Element Is Visible   id:tag
    Scroll Element Into View         id:tag
    Input Text  tag  Lukematta
    Click Save Button
    Wait Until Page Contains  Reference added
    Go To  ${HOME_URL}
    Wait Until Page Contains  @book{ book-1
    Wait Until Page Contains  tag = { Lukematta }

