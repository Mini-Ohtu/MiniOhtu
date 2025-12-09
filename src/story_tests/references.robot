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
    Click Save Button
    Wait Until Page Contains  Reference added

Invalid year shows an error
    Go To  ${HOME_URL}
    Click Link  Create new reference
    Input Text  citekey  bad-year
    Input Text  author  Bad Year Author
    Input Text  title  Bad Year Title
    Input Text  year  not-a-year
    Input Text  publisher  Bad Pub
    Click Save Button
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
    Click Save Button
    Wait Until Page Contains  Reference added
    Go To  ${HOME_URL}
    Wait Until Page Contains  @article{ article-1
    Wait Until Page Contains  journal = { Journal Name }
    Wait Until Page Contains  volume = { 10 }

Article creation shows up in list
    Go To  ${HOME_URL}
    Click Link  Create new reference
    Click Element  entry_type_article
    Input Text  citekey  article-show
    Input Text  author  Show Author
    Input Text  title  Show Title
    Input Text  journal  Show Journal
    Input Text  year  2022
    Click Save Button
    Wait Until Page Contains  Reference added
    Go To  ${HOME_URL}
    Wait Until Page Contains  @article{ article-show
    Wait Until Page Contains  Show Journal

Missing required article field shows error
    Go To  ${HOME_URL}
    Click Link  Create new reference
    Click Element  entry_type_article
    Input Text  citekey  article-missing
    Input Text  author  Missing Journal Author
    Input Text  title  Missing Journal Title
    Input Text  journal  ${SPACE}
    Input Text  year  2024
    Click Save Button
    Wait Until Page Contains  journal is required

Site does not show reference after deleting it
    Go To  ${HOME_URL}
    Click Link  Create new reference
    Input Text  citekey  deleting
    Input Text  author  Book Author
    Input Text  title  Book to delete
    Input Text  year  2023
    Input Text  publisher  Book Publisher
    Click Save Button
    Wait Until Page Contains  Reference added
    Go To  ${HOME_URL}
    Click Button  Delete
    Handle Alert
    Page Should Not Contain  Book to delete

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

Deleting a reference shows confirmation alert
    Go To  ${HOME_URL}
    Click Link  Create new reference
    Input Text  citekey  Smith2020
    Input Text  author  John Smith
    Input Text  title  Web development
    Input Text  year  2020
    Input Text  publisher  TechPress
    Click Save Button
    Wait Until Page Contains  Reference added
    Go To  ${HOME_URL}
    Wait Until Page Contains  @book{ Smith2020
    Click Button  Delete
    ${message} =  Handle Alert  LEAVE
    Should Be Equal  ${message}  Are you sure you want to delete this reference?
    Handle Alert
    Page Should Not Contain  Smith2020

*** Keywords ***
Citekey Should Match Pattern
    [Arguments]  ${pattern}
    ${value}=  Get Value  id:citekey
    Should Match Regexp  ${value}  ${pattern}
