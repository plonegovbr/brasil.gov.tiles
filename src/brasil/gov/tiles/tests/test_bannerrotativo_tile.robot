*** Settings ***

Resource  collective/cover/tests/cover.robot
Library  Remote  ${PLONE_URL}/RobotRemote

Suite Setup  Open Test Browser
Suite Teardown  Close all browsers

*** Variables ***

${filter_items}  contentchooser-content-trees
${banner_rotativo_tile_location}  'banner_rotativo'
${item_to_remove}  li#banner4 i.tile-remove-item
${removed_item}  li#banner4 a.banner
${item_to_move}  li#banner1 a.banner
${location_to_move}  li#banner3 a.banner
# Como funciona o teste? Coloco o xpath de onde o primeiro item do banner,
# que tem um span de texto 'my-image', deve ficar após ter ser movido, ou seja,
# no lugar do terceiro banner, definido na variável ($location_to_move)
${location_item_moved}  //ul[@id='tile_banner_rotativo']/li[@id='banner3']/a[@class='banner']/span[contains(text(), 'my-image')]
${collection_selector}  li.ui-draggable a.contenttype-collection
${tile_selector}  div.tile-container div.tile

*** Test cases ***

Test Banner Rotativo Tile
    Enable Autologin as  Site Administrator
    Go to Homepage
    Create Cover  Title  Description  Empty layout

    # add a banner_rotativo tile to the layout
    Open Layout Tab
    Wait until page contains  Export layout
    Add Tile  ${banner_rotativo_tile_location}
    Save Cover Layout

    # as tile is empty, we see default message
    Compose Cover
    Page Should Contain  Rotating Banner

    # drag&drop an image collection
    Open Content Chooser
    Click Link  link=Content tree
    Drag And Drop  css=${collection_selector}  css=${tile_selector}
    Wait Until Page Contains Element  css=li#banner1 a.banner, li#banner2 a.banner, li#banner3 a.banner, li#banner4 a.banner

    # move to the default view and check tile persisted
    Click Link  link=View
    Page Should Contain Element  css=li#banner1 a.banner, li#banner2 a.banner, li#banner3 a.banner, li#banner4 a.banner

    # remove an item from the banner
    Compose Cover
    Click Element  css=${item_to_remove}
    # Coloco o sleep pro AJAX da deleção e renderização na mesma tela.
    Sleep  1s
    Page Should Not Contain Element  css=${removed_item}

    # move the first banner item to the last position
    Drag And Drop  css=${item_to_move}  css=${location_to_move}
    # Coloco o sleep pro AJAX da deleção e renderização na mesma tela.
    Sleep  1s
    Page Should Contain Element  xpath=${location_item_moved}

    # delete the tile
    Open Layout Tab
    Delete Tile
    Save Cover Layout
