*** Settings ***
Library    SeleniumLibrary
Library    ../chromedriver_wrapper.py
Resource   ../resources/login_page.resource

Suite Setup       Open Browser To Login Page
Suite Teardown    Close Browser

*** Variables ***
${URL}            https://accounts2.netgear.com/login?redirectUrl=https:%2F%2Finsight.netgear.com%2F&clientId=6dlf5ppqm5oic7hhtk68qrlc9j
${USERNAME}       viku.prod@yopmail.com
${PASSWORD}       Netgear1@

*** Keywords ***
Open Browser To Login Page
    ${options}=    Chrome Options
    Open Browser    ${URL}    chrome    options=${options}
    Maximize Browser Window
    Sleep    3s

*** Test Cases ***
Login With Valid Credentials
    Enter The Username    ${USERNAME}
    Enter The Password    ${PASSWORD}
    Click On Sign In Button