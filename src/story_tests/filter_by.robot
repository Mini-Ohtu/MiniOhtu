*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Database

*** Test Cases ***

After adding a book show confirmation 22
    Go To  ${POPULATE_DB_URL}
    Click Link  Create new reference
    Input Text  citekey  book-test
    Input Text  author  Test Author
    Input Text  title  Test Title
    Input Text  year  2024
    Input Text  publisher  Test Publisher
    Click Save Button
    Wait Until Page Contains  Reference added