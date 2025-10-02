*** Settings ***
Library    SeleniumLibrary
Library    ../chromedriver_wrapper.py

*** Variables ***
${URL}    https://example.com

*** Keywords ***
Open Browser To Example
    ${options}=    Chrome Options
    Open Browser    ${URL}    chrome    options=${options}
    Maximize Browser Window
    Sleep    1s

*** Test Cases ***
Verify Example Page Title
    [Setup]    Open Browser To Example
    Title Should Be    Example Domain
    [Teardown]    Close Browser

Verify Example Content
    [Setup]    Open Browser To Example
    Element Should Be Visible    xpath://h1[contains(text(), 'Example Domain')]
    [Teardown]    Close Browser

Log Example Domain
    Log To Console    Example Domain