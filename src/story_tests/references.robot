*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Database

*** Variables ***
&{BOOKLET_FIELDS}=    title=Booklet Title    author=Pamphlet Author    howpublished=Leaflet Distribution    year=2024
&{CONFERENCE_FIELDS}=    author=Conf Author    title=Conference Paper    booktitle=TestingConf    year=2022    pages=12-20
&{INBOOK_FIELDS}=    author=Inbook Author    editor=Inbook Editor    title=Inbook Title    chapter=3    pages=33-55    publisher=Inbook Publisher    year=2021    edition=Second
&{INCOLLECTION_FIELDS}=    author=Collection Author    title=Collection Title    booktitle=Collected Works    publisher=Collection Publisher    year=2020    chapter=2
&{INPROCEEDINGS_FIELDS}=    author=Inproc Author    title=Inproc Title    booktitle=Proceedings on Testing    year=2019    organization=QA Org
&{MANUAL_FIELDS}=    title=Manual Title    author=Manual Author    organization=Manual Org    year=2018
&{MASTERSTHESIS_FIELDS}=    author=Masters Student    title=Masters Thesis    school=University of Testing    year=2023    type=Pro gradu
&{MISC_FIELDS}=    author=Misc Author    title=Misc Title    howpublished=Online    year=2024
&{PHDTHESIS_FIELDS}=    author=PhD Author    title=PhD Thesis    school=Tech University    year=2017    address=Helsinki
&{PROCEEDINGS_FIELDS}=    title=Proceedings Title    year=2016    editor=Series Editor    publisher=Publisher House
&{TECHREPORT_FIELDS}=    author=Reporter    title=Technical Report    institution=Tech Institute    year=2015    number=TR-15
&{UNPUBLISHED_FIELDS}=    author=Unpub Author    title=Draft Work    note=Submitted soon    year=2014

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

Booklet reference can be created
    Create Reference With Fields  booklet  booklet-robot  &{BOOKLET_FIELDS}

Conference reference can be created
    Create Reference With Fields  conference  conference-robot  &{CONFERENCE_FIELDS}

Inbook reference can be created
    Create Reference With Fields  inbook  inbook-robot  &{INBOOK_FIELDS}

Incollection reference can be created
    Create Reference With Fields  incollection  incollection-robot  &{INCOLLECTION_FIELDS}

Inproceedings reference can be created
    Create Reference With Fields  inproceedings  inproceedings-robot  &{INPROCEEDINGS_FIELDS}

Manual reference can be created
    Create Reference With Fields  manual  manual-robot  &{MANUAL_FIELDS}

Mastersthesis reference can be created
    Create Reference With Fields  mastersthesis  mastersthesis-robot  &{MASTERSTHESIS_FIELDS}

Misc reference can be created
    Create Reference With Fields  misc  misc-robot  &{MISC_FIELDS}

Phdthesis reference can be created
    Create Reference With Fields  phdthesis  phd-robot  &{PHDTHESIS_FIELDS}

Proceedings reference can be created
    Create Reference With Fields  proceedings  proceedings-robot  &{PROCEEDINGS_FIELDS}

Techreport reference can be created
    Create Reference With Fields  techreport  techreport-robot  &{TECHREPORT_FIELDS}

Unpublished reference can be created
    Create Reference With Fields  unpublished  unpublished-robot  &{UNPUBLISHED_FIELDS}

Reference can be created via DOI prefill
    Go To  ${HOME_URL}
    Click Link  Create new reference
    Wait Until Element Is Visible  id:doi-input
    Input Text  id:doi-input  robot-doi/1234
    Click Button  Fill from DOI
    Wait Until Element Is Visible  id:citekey
    ${prefilled_citekey}=  Get Value  id:citekey
    Should Be Equal  ${prefilled_citekey}  Robot_Doi_2024
    Radio Button Should Be Set To  entry_type  article
    Wait Until Element Is Visible  id:title
    ${prefilled_title}=  Get Value  id:title
    Should Be Equal  ${prefilled_title}  Robot DOI Article
    ${prefilled_author}=  Get Value  id:author
    Should Be Equal  ${prefilled_author}  Robo Tester
    Click Save Button
    Wait Until Page Contains  Reference added
    Go To  ${HOME_URL}
    Wait Until Page Contains  @article{ Robot_Doi_2024
    Wait Until Page Contains  journal = { Automation Letters }
    Wait Until Page Contains  author = { Robo Tester }

*** Keywords ***

Create Reference With Fields
    [Arguments]  ${entry_type}  ${citekey}  &{fields}
    Go To  ${HOME_URL}
    Click Link  Create new reference
    Wait Until Element Is Visible  entry_type_${entry_type}
    Click Element  entry_type_${entry_type}
    Input Text  citekey  ${citekey}
    FOR  ${name}  ${value}  IN  &{fields}
        Wait Until Element Is Visible  id:${name}
        Scroll Element Into View      id:${name}
        Input Text  ${name}  ${value}
    END
    Click Save Button
    Wait Until Page Contains  Reference added
    Go To  ${HOME_URL}
    Wait Until Page Contains  @${entry_type}{ ${citekey}
    FOR  ${name}  ${value}  IN  &{fields}
        Wait Until Page Contains  ${name} = { ${value} }
    END
