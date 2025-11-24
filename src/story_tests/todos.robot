*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Database

*** Test Cases ***

After adding a book show confirmation
    Go To  ${HOME_URL}
    Click Link  Create new reference
    Input Text  citekey  book-test
    Input Text  author  Test Author
    Input Text  title  Test Title
    Input Text  year  2024
    Input Text  publisher  Test Publisher
    Click Button  Save
    Wait Until Page Contains  Reference added

Invalid year shows an error
    Go To  ${HOME_URL}
    Click Link  Create new reference
    Input Text  citekey  bad-year
    Input Text  author  Bad Year Author
    Input Text  title  Bad Year Title
    Input Text  year  not-a-year
    Input Text  publisher  Bad Pub
    Click Button  Save
    Wait Until Page Contains  Year must be an integer

Article type requires its own fields
    Go To  ${HOME_URL}
    Click Link  Create new reference
    Click Element  entry_type_article
    Input Text  citekey  article-1
    Input Text  author  Article Author
    Input Text  title  Article Title
    Input Text  journal  Journal Name
    Input Text  year  2023
    Input Text  volume  10
    Input Text  pages  100-110
    Click Button  Save
    Wait Until Page Contains  Reference added
    Go To  ${HOME_URL}
    Wait Until Page Contains  @article{ article-1
    Wait Until Page Contains  journal = { Journal Name }
    Wait Until Page Contains  volume = { 10 }
