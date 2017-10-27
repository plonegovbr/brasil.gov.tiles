*** Settings ***

Resource  collective/cover/tests/cover.robot
Library  Remote  ${PLONE_URL}/RobotRemote

Suite Setup  Open Test Browser
Suite Teardown  Close all browsers

*** Variables ***

${header_tile_location}  "standaloneheader"
${collection_selector}  .ui-draggable .contenttype-collection
${tile_selector}  div.tile-container div.tile
${edit_link_selector}  a.edit-tile-link
${title_field_id}  standaloneheader-title
${link_text_field_id}  standaloneheader-link_text
${link_url_field_id}  standaloneheader-link_url
${title_sample}  Some text for title
${title_other_sample}  This text should never be saved
${link_text_sample}  Plone
${link_text_other_sample}  Google
${link_url_sample}  http://www.plone.org
${link_url_other_sample}  http://www.google.com

*** Test cases ***

Test Header Tile
    [Setup]  Set Selenium Speed  .5

    Enable Autologin as  Site Administrator
    Go to Homepage
    Create Cover  Title  Description  Empty layout

    # add a headers tile to the layout
    Open Layout Tab
    Add Tile  ${header_tile_location}
    Save Cover Layout

    # as tile is empty
    Compose Cover
    Page Should Contain Element  css=div.outstanding-header

    # drag&drop an Collection
    Open Content Chooser
    Drag And Drop  css=${collection_selector}  css=${tile_selector}
    Wait Until Page Contains Element  css=div.outstanding-header
    Wait Until Page Contains Element  css=a.outstanding-link

    # move to the default view and check tile persisted
    Click Link  link=View
    Wait Until Page Contains Element  css=div.outstanding-header

    # edit and check AJAX refresh
    Compose Cover
    Click Link  css=${edit_link_selector}
    Page Should Contain Element  css=#${title_field_id}
    Input Text  id=${title_field_id}  ${title_sample}
    Input Text  id=${link_text_field_id}  ${link_text_sample}
    Input Text  id=${link_url_field_id}  ${link_url_sample}
    Click Button  Save
    Wait Until Page Contains  ${title_sample}
    Wait Until Page Contains  ${link_text_sample}

    # edit but cancel operation
    Compose Cover
    Click Link  css=${edit_link_selector}
    Page Should Contain Element  css=#${title_field_id}
    Input Text  id=${title_field_id}  ${title_other_sample}
    Input Text  id=${link_text_field_id}  ${link_text_other_sample}
    Input Text  id=${link_url_field_id}  ${link_url_other_sample}
    Click Button  Cancel
    Wait Until Page Contains  ${title_sample}
    Wait Until Page Contains  ${link_text_sample}

    # delete the tile
    Open Layout Tab
    Delete Tile
    Save Cover Layout
