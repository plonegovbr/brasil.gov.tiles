*** Settings ***

Resource  collective/cover/tests/cover.robot
Library  Remote  ${PLONE_URL}/RobotRemote

Suite Setup  Open Test Browser
Suite Teardown  Close all browsers

*** Variables ***

${filter_items}  contentchooser-content-trees
${destaque_tile_location}  'destaque'
${collection_selector}  li.ui-draggable a.contenttype-collection
${tile_selector}  div.tile-container div.tile

*** Keywords ***

# FIXME: Nova keyword adicionada, uma vez que a original do cover presente em 
# https://github.com/collective/collective.cover/blob/dfd128a1ca6a75edc5f5190919bcffe7c9b4182f/src/collective/cover/tests/cover.robot#L88
# pega o tile errado: o uso do contains em xpath está pegando o 'em_destaque' ao
# invés do 'destaque' pois pega também substring.
# Isso foi corrigido no collective.cover em
# https://github.com/collective/collective.cover/pull/715/commits/cac230c0621d70b7ce8b1befb7efd457f688e281
# Mas só poderá ser usado a partir da versão 1.4b2.
Add Destaque Tile
    [arguments]  ${tile}

    Drag And Drop  xpath=//a[@data-tile-type=${tile}]  css=${tile_drop_area_selector}
    Wait Until Page Contains Element  css=.tile-name

*** Test cases ***

Test Destaque Tile
    Enable Autologin as  Site Administrator
    Go to Homepage
    Create Cover  Title  Description  Empty layout

    # add a destaque tile to the layout
    Open Layout Tab
    Wait until page contains  Export layout
    Add Destaque Tile  ${destaque_tile_location}
    Save Cover Layout

    # as tile is empty, we see default message
    Compose Cover
    Page Should Contain  Please add up to 2 objects to the tile

    # drag&drop a collection
    Open Content Chooser
    Click Link  link=Content tree
    Drag And Drop  css=${collection_selector}  css=${tile_selector}
    Wait Until Page Contains Element  css=div.items-destaque
    Wait Until Page Contains Element  css=div.items-destaque div.item a h1

    # move to the default view and check tile persisted
    Click Link  link=View
    Page Should Contain Element  css=div.items-destaque
    Page Should Contain Element  css=div.items-destaque div.item a h1

    # delete the tile
    Open Layout Tab
    Delete Tile
    Save Cover Layout
