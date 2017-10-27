*** Settings ***

Resource  collective/cover/tests/cover.robot
Library  Remote  ${PLONE_URL}/RobotRemote

Suite Setup  Open Test Browser
Suite Teardown  Close all browsers

*** Variables ***

${albuns_tile_location}  "albuns"
${content_tree}  .formTabs .formTab:nth-child(2) a
${folder_selector}  .ui-draggable .contenttype-folder
${tile_selector}  div.tile-container div.tile
${edit_link_selector}  a.edit-tile-link
${title_field_id}  albuns-title
${title_sample}  Some text for title
${title_other_sample}  This text should never be saved
${footertext_field_id}  albuns-link_text
${footerurl_field_id}  albuns-link_url
${footertext_sample}  Plone
${footerurl_sample}  http://www.plone.org
${footertext_other_sample}  Google
${footerurl_other_sample}  http://www.google.com

*** Test cases ***

Test Albuns Tile
    [Setup]  Set Selenium Speed  .5

    Enable Autologin as  Site Administrator
    Go to Homepage
    Create Cover  Title  Description  Empty layout

    # add a albuns tile to the layout
    Open Layout Tab
    Add Tile  ${albuns_tile_location}
    Save Cover Layout

    # as tile is empty, we see default message
    Compose Cover
    Page Should Contain  Drag an album to the popular tile.

    # drag&drop an Album
    # FIXME: Need to enable albuns and create an album content
    Open Content Chooser
    Click Link  css=${content_tree}
    Drag And Drop  css=${folder_selector}  css=${tile_selector}
    Wait Until Page Contains Element  css=div.album-tile
    Page Should Contain  Drag an album to the popular tile.

    # move to the default view and check tile persisted
    # FIXME: Need to enable albuns and create an album content
    Click Link  link=View
    Wait Until Page Contains Element  css=div.album-tile
    Page Should Contain  Drag an album to the popular tile.

    # edit the title and check AJAX refresh
    Compose Cover
    Click Link  css=${edit_link_selector}
    Page Should Contain Element  css=#${title_field_id}
    Input Text  id=${title_field_id}  ${title_sample}
    Click Button  Save
    Wait Until Page Contains  ${title_sample}

    # edit the title but cancel operation
    Compose Cover
    Click Link  css=${edit_link_selector}
    Page Should Contain Element  css=#${title_field_id}
    Input Text  id=${title_field_id}  ${title_other_sample}
    Click Button  Cancel
    Wait Until Page Contains  ${title_sample}

    # edit the footer text and check AJAX refresh
    Compose Cover
    Click Link  css=${edit_link_selector}
    Page Should Contain Element  css=#${footertext_field_id}
    Input Text  id=${footertext_field_id}  ${footertext_sample}
    Page Should Contain Element  css=#${footerurl_field_id}
    Input Text  id=${footerurl_field_id}  ${footerurl_sample}
    Click Button  Save
    Wait Until Page Contains  ${footertext_sample}

    # edit the footer text but cancel operation
    Compose Cover
    Click Link  css=${edit_link_selector}
    Page Should Contain Element  css=#${footertext_field_id}
    Input Text  id=${footertext_field_id}  ${footertext_other_sample}
    Page Should Contain Element  css=#${footerurl_field_id}
    Input Text  id=${footerurl_field_id}  ${footerurl_other_sample}
    Click Button  Cancel
    Wait Until Page Contains  ${footertext_sample}

    # delete the tile
    Open Layout Tab
    Delete Tile
    Save Cover Layout
