*** Settings ***

Resource  collective/cover/tests/cover.robot
Library  Remote  ${PLONE_URL}/RobotRemote

Suite Setup  Open Test Browser
Suite Teardown  Close all browsers

*** Variables ***

${filter_items}  contentchooser-content-trees
${em_destaque_tile_location}  'em_destaque'
${collection_selector}  li.ui-draggable a.contenttype-collection
${tile_selector}  div.tile-container div.tile

*** Test cases ***

Test Em Destaque Tile
    Enable Autologin as  Site Administrator
    Go to Homepage
    Create Cover  Title  Description  Empty layout

    # add an em destaque tile to the layout
    Open Layout Tab
    Wait until page contains  Export layout
    Add Tile  ${em_destaque_tile_location}
    Save Cover Layout

    # as tile is empty, we see default message
    Compose Cover
    Page Should Contain  Please add up to 5 objects to the tile

    # drag&drop a collection
    Open Content Chooser
    Click Link  link=Content tree
    Drag And Drop  css=${collection_selector}  css=${tile_selector}
    Wait Until Page Contains Element  css=div#em-destaque ul li#em-destaque-titulo
    Wait Until Page Contains Element  css=div#em-destaque ul li a

    # move to the default view and check tile persisted
    Click Link  link=View
    Page Should Contain Element  css=div#em-destaque ul li#em-destaque-titulo
    Page Should Contain Element  css=div#em-destaque ul li a

    # delete the tile
    Open Layout Tab
    Delete Tile
    Save Cover Layout
