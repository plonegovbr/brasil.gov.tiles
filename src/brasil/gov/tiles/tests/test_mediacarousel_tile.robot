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
    Page Should Contain  Arraste uma pasta ou coleção para popular o tile.

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
