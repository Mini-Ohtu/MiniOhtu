*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Database

*** Test Cases ***

After adding a book show confirmation
    Go To  ${HOME_URL}
    Click Link  Create new book
    Input Text  author  Test Author
    Input Text  title  Test Title
    Input Text  year  2024
    Input Text  publisher  Test Publisher
    Click Button  Save
    Wait Until Page Contains  Book added

Invalid year shows an error
    Go To  ${HOME_URL}
    Click Link  Create new book
    Input Text  author  Bad Year Author
    Input Text  title  Bad Year Title
    Input Text  year  not-a-year
    Input Text  publisher  Bad Pub
    Click Button  Save
    Wait Until Page Contains  Year must be an integer