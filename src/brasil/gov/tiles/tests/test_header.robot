*** Settings ***

Resource  collective/cover/tests/cover.robot
Library  Remote  ${PLONE_URL}/RobotRemote

Suite Setup  Open Test Browser
Suite Teardown  Close all browsers

*** Variables ***

${filter_items}  contentchooser-content-trees
${header_tile_location}  "standaloneheader"
${folder_selector}  .ui-draggable .contenttype-folder
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

*** Keywords ***

# FIXME: Customização de cover.robot em collective cover para poder aplicar a solução
# presente em http://www.coactivate.org/projects/barcelona-sprint/lists/barcelona-sprint-discussion/archive/2013/02/1360419825199/forum_view
# corrigindo o erro StaleElementReferenceException: Message: Element not found in the cache - perhaps the page has changed since it was looked up
# Ver https://github.com/plonegovbr/brasil.gov.tiles/pull/128#issuecomment-102429107
# O mais correto seria corrigir em collective.cover, daí o FIXME. Isso está em estudo.
Compose Cover
    [Documentation]  Click on Compose tab and wait until the layout has been
    ...              loaded.
    Wait Until Keyword Succeeds  5 sec  1 sec  Click Link  link=Compose
    Sleep  1s  Wait for cover compose to load
    Wait Until Page Contains Element  css=div#contentchooser-content-show-button
    Page Should Contain  Add Content

# FIXME: Customização de cover.robot em collective cover para poder aplicar a solução
# https://github.com/collective/collective.cover/commit/0d4c0ba8ba1f7c61d77e8b766d48a74b388b6269
# Ver https://github.com/collective/collective.cover/issues/582#issuecomment-173333865
# O mais correto seria corrigir em collective.cover, daí o FIXME. Isso está em estudo.
Edit Cover Layout
    [Documentation]  Click on Layout tab and wait until the layout has been
    ...              loaded. Buttons related with layout operations must be
    ...              also visible.
    Wait Until Keyword Succeeds  10 sec  2 sec  Click Link  link=Layout
    Sleep  1s  Wait for cover layout to load
    Wait until page contains  Export layout
    Wait until page contains  Saved

*** Test cases ***

Test Header Tile
    Enable Autologin as  Site Administrator
    Go to Homepage
    Create Cover  Title  Description  Empty layout

    # add a headers tile to the layout
    Edit Cover Layout
    Add Tile  ${header_tile_location}
    Save Cover Layout

    # as tile is empty
    Compose Cover
    Page Should Contain Element  css=div.outstanding-header

    # drag&drop an Header
    # FIXME: Need to enable headers and create an header content
    Open Content Chooser
    Click Link  css=${content_tree}
    Drag And Drop  css=${folder_selector}  css=${tile_selector}
    Wait Until Page Contains Element  css=div.outstanding-header

    # move to the default view and check tile persisted
    # FIXME: Need to enable headers and create an header content
    Click Link  link=View
    Wait Until Page Contains Element  css=div.outstanding-header

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
    Page Should Contain Element  css=#${link_text_field_id}
    Input Text  id=${link_text_field_id}  ${link_text_sample}
    Page Should Contain Element  css=#${link_url_field_id}
    Input Text  id=${link_url_field_id}  ${link_url_sample}
    Click Button  Save
    Wait Until Page Contains  ${link_text_sample}

    # edit the footer text but cancel operation
    Compose Cover
    Click Link  css=${edit_link_selector}
    Page Should Contain Element  css=#${link_text_field_id}
    Input Text  id=${link_text_field_id}  ${link_text_sample}
    Page Should Contain Element  css=#${link_url_field_id}
    Input Text  id=${link_url_field_id}  ${link_url_other_sample}
    Click Button  Cancel
    Wait Until Page Contains  ${link_text_sample}

    # delete the tile
    Edit Cover Layout
    Delete Tile
    Save Cover Layout
