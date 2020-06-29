*** Settings ***
Library           SeleniumLibrary

*** Variables ***
${base_url}       http://127.0.0.1:5000/
${pid}            100000001    # Patient ID
${ssnid}          789456123
${HOSP_NAME}      ABC Hospital
${REG_EXEC_USERNAME}    admin
${REG_EXEC_PASSWORD}    admin
${PHARMACIST_USERNAME}    admin2
${PHARMACIST_PASSWORD}    admin
${DIAGNOSTIC_USERNAME}    admin3
${DIAGNOSTIC_PASSWORD}    admin

*** Test Cases ***
test_registration_executive_login
    Open Browser    ${base_url}    chrome
    Maximize Browser Window
    RegExecutive Login Page Should Be Open
    Click Link    Logout
    Close Browser

test_pharmacist_login
    Open Browser    ${base_url}    chrome
    Maximize Browser Window
    Pharmacist Login Page Should Be Open
    Click Link    Logout
    Close Browser

test_diagnostic_login
    Open Browser    ${base_url}    chrome
    Maximize Browser Window
    Diagnostic Login Page Should Be Open
    Click Link    Logout
    Close Browser

test_create_update_delete_patient
    Open Browser    ${base_url}    chrome
    Maximize Browser Window
    RegExecutive Login Page Should Be Open
    Click Element    //*[contains(text(),'Patient Management')]
    Click Link    Create Patient
    Title Should Be    ${HOSP_NAME} | Create Patient
    Input Text    name:ssnid    ${ssnid}
    Input Text    name:pname    Sainath
    Input Text    name:page    22
    Select From List By Value    name:type_of_bed    single_room
    Input Text    name:paddress    Charlapally
    Execute Javascript    window.scrollTo(0,200)
    Select From List By Label    name:pstate    Andhra Pradesh
    Select From List By Label    name:pcity    Hyderabad
    Execute Javascript    window.scrollTo(0,300)
    Click Button    Create
    Set Selenium Speed    0.2 seconds
    Click Element    //*[contains(text(),'Patient Management')]
    Click Link    Edit Patient
    Title Should Be    ${HOSP_NAME} | Update Patient
    Input Text    id:pid_for_search    ${pid}
    Click Button    GET
    Sleep    2s
    Input Text    name:pname    Sainath Omdas
    Execute Javascript    window.scrollTo(0,200)
    Input Text    name:page    22
    Execute Javascript    window.scrollTo(0,200)
    Select From List By Value    name:type_of_bed    semi_sharing
    Input Text    name:paddress    ECIL
    Execute Javascript    window.scrollTo(0,200)
    Select From List By Label    name:pstate    Andhra Pradesh
    Select From List By Label    name:pcity    Hyderabad
    Execute Javascript    window.scrollTo(0,300)
    Click Button    Update
    Title Should Be    ${HOSP_NAME} | Update Patient
    Click Element    //*[contains(text(),'Patient Management')]
    Click Link    Delete Patient
    Title Should Be    ${HOSP_NAME} | Delete Patient
    Input Text    id:pid_for_search    ${pid}
    Click Button    GET
    Sleep    0.5s
    Click Link    Logout
    Close Browser

test_view_patients
    Open Browser    ${base_url}    chrome
    Maximize Browser Window
    RegExecutive Login Page Should Be Open
    Click Element    //*[contains(text(),'View Patients')]
    Title Should Be    ${HOSP_NAME} | View Patients
    Sleep    2s
    Click Link    Logout
    Close Browser

test_search_patient
    Open Browser    ${base_url}    chrome
    Maximize Browser Window
    RegExecutive Login Page Should Be Open
    Click Element    //*[contains(text(),'Search Patient')]
    Title Should Be    ${HOSP_NAME} | Search Patient
    Input Text    id:pid_for_search    ${pid}
    Click Button    GET
    Sleep    2s
    Click Link    Logout
    Close Browser

test_billing
    Open Browser    ${base_url}    chrome
    Maximize Browser Window
    RegExecutive Login Page Should Be Open
    Click Link    Billing
    Title Should Be    ${HOSP_NAME} | Billing
    Input Text    id:pid_for_search    ${pid}
    Click Button    GET
    Sleep    2s
    Execute Javascript    window.scrollTo(0,200)
    Execute Javascript    window.scrollTo(0,200)
    Execute Javascript    window.scrollTo(0,200)
    Execute Javascript    window.scrollTo(0,200)
    Execute Javascript    window.scrollTo(0,200)
    Click Link    Logout
    Close Browser

test_pharmacist_tasks
    Open Browser    ${base_url}    chrome
    Maximize Browser Window
    Go To Pharmacist Login Page
    Click Link    Issue Medicines
    Title Should Be    ${HOSP_NAME} | Issued Medicines
    Input Text    id:pid_for_search    ${pid}
    Click Button    GET
    Sleep    1s
    Execute Javascript    location.href = "#issueMedicinesBtn"
    Click Element    id:issueMedicinesBtn
    Title Should Be    ${HOSP_NAME} | Issue New Medicines
    Select From List By Value    name:medicine_id    3
    Click Button    GET
    Input Text    id:qty    1
    Click Button    Add
    Select From List By Value    name:medicine_id    5
    Click Button    GET
    Input Text    id:qty    1
    Click Button    Add
    Execute Javascript    location.href = "#issueBtn"
    Click Element    id:issueBtn
    Sleep    1s
    Click Link    Logout
    Close Browser

test_diagnostic_tasks
    [Tags]    t
    Open Browser    ${base_url}    chrome
    Maximize Browser Window
    Go To Diagnostic Login Page
    Click Link    Diagnostics
    Title Should Be    ${HOSP_NAME} | Diagnostics
    Input Text    id:pid_for_search    ${pid}
    Click Button    GET
    Sleep    1s
    Execute Javascript    location.href = "#addDiagnosticsBtn"
    Click Element    id:addDiagnosticsBtn
    Title Should Be    ${HOSP_NAME} | Add Diagnostics
    Select From List By Value    name:diagnostic_test    3
    Click Button    Add
    Select From List By Value    name:diagnostic_test    5
    Click Button    Add
    Execute Javascript    location.href = "#addTestsBtn"
    Click Element    id:addTestsBtn
    Sleep    1s
    Click Link    Logout
    Close Browser

*** Keywords ***
Go To RegExecutive Login Page
    RegExecutive Login Page Should Be Open

RegExecutive Login Page Should Be Open
    Title Should Be    ABC Hospital | Login
    Input Text    name:username    ${REG_EXEC_USERNAME}
    Input Text    name:password    ${REG_EXEC_PASSWORD}
    Select From List By Value    name:login_type    reg
    Click Button    Login
    Title Should Be    ABC Hospital | Home

Go To Pharmacist Login Page
    Pharmacist Login Page Should Be Open

Pharmacist Login Page Should Be Open
    Title Should Be    ABC Hospital | Login
    Input Text    name:username    ${PHARMACIST_USERNAME}
    Input Text    name:password    ${PHARMACIST_PASSWORD}
    Select From List By Value    name:login_type    pharm
    Click Button    Login
    Title Should Be    ABC Hospital | Home

Go To Diagnostic Login Page
    Diagnostic Login Page Should Be Open

Diagnostic Login Page Should Be Open
    Title Should Be    ABC Hospital | Login
    Input Text    name:username    ${DIAGNOSTIC_USERNAME}
    Input Text    name:password    ${DIAGNOSTIC_PASSWORD}
    Select From List By Value    name:login_type    diag
    Click Button    Login
    Title Should Be    ABC Hospital | Home
