*** Settings ***

Resource  collective/cover/tests/cover.robot
Library  Remote  ${PLONE_URL}/RobotRemote

Suite Setup  Open Test Browser
Suite Teardown  Close all browsers

*** Variables ***

${mediacarousel_tile_location}  'mediacarousel'
${collection_selector}  .ui-draggable .contenttype-collection
${tile_selector}  div.tile-container div.tile
${edit_link_selector}  a.edit-tile-link
${title_field_id}  mediacarousel-header
${title_sample}  Some text for title
${title_other_sample}  This text should never be saved
${footer_field_id}  mediacarousel-footer_text
${footer_sample}  http://www.plone.org
${footer_other_sample}  http://www.google.com

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

*** Test cases ***

Test Mediacarousel Tile
    Enable Autologin as  Site Administrator
    Go to Homepage
    Create Cover  Title  Description  Empty layout

    # add a mediacarousel tile to the layout
    Edit Cover Layout
    Page Should Contain  Export layout
    Add Tile  ${mediacarousel_tile_location}
    Save Cover Layout

    # as tile is empty, we see default message
    Compose Cover
    Page Should Contain  Drag a folder or collection to populate the tile.

    # drag&drop an Collection
    Open Content Chooser
    Drag And Drop  css=${collection_selector}  css=${tile_selector}
    Wait Until Page Contains Element  css=div.mediacarousel.tile-content h2.mediacarousel-tile+div

    # move to the default view and check tile persisted
    Click Link  link=View
    Page Should Contain Element  css=div.mediacarousel.tile-content h2.mediacarousel-tile

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

    # edit the footer and check AJAX refresh
    Compose Cover
    Click Link  css=${edit_link_selector}
    Sleep  1s  Wait for overlay
    Page Should Contain Element  css=#${footer_field_id}
    Input Text  id=${footer_field_id}  ${footer_sample}
    Click Button  Save
    Wait Until Page Contains  ${footer_sample}

    # edit the footer but cancel operation
    Compose Cover
    Click Link  css=${edit_link_selector}
    Sleep  1s  Wait for overlay
    Page Should Contain Element  css=#${footer_field_id}
    Input Text  id=${footer_field_id}  ${footer_other_sample}
    Click Button  Cancel
    Wait Until Page Contains  ${footer_sample}

    # delete the tile
    Edit Cover Layout
    Delete Tile
    Save Cover Layout
