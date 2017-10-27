*** Settings ***

Resource  collective/cover/tests/cover.robot
Library  Remote  ${PLONE_URL}/RobotRemote

Suite Setup  Open Test Browser
Suite Teardown  Close all browsers

*** Variables ***

${filter_items}  contentchooser-content-trees
${my_news_folder}  my-news-folder
${mediacarousel_tile_location}  'mediacarousel'
${collection_selector}  .ui-draggable .contenttype-collection
# This xpath selector is for the <a> father of <span>my-news-folder</span>
${my_news_folder_selector}  //span[contains(text(),'my-news-folder')]/..
${title_nitf_with_image}  my-nitf-with-image
${title_nitf_without_image}  my-nitf-without-image
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
    [Setup]  Set Selenium Speed  .5

    Enable Autologin as  Site Administrator
    Go to Homepage
    Create Cover  Title  Description  Empty layout

    # add a mediacarousel tile to the layout
    Open Layout Tab
    Wait until page contains  Export layout
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
    Open Layout Tab
    Delete Tile
    Save Cover Layout

    # add a mediacarousel tile to the layout
    Open Layout Tab
    Wait until page contains  Export layout
    Add Tile  ${mediacarousel_tile_location}
    Save Cover Layout

    # as tile is empty, we see default message
    Compose Cover
    Page Should Contain  Drag a folder or collection to populate the tile.

    # drag&drop a folder with nitf content
    Open Content Chooser
    Click Link  link=Content tree
    # Temos um bug no robots onde ele não consegue selecionar um ícone do overlay
    # "Adicionar conteúdo" se for necessário usar o scroll, era como se ele não
    # conseguisse "ver" o objeto: dessa forma, uso o filtro de items para mostrar
    # menos itens e evitar esse problema.
    # FIXME: https://github.com/robotframework/Selenium2Library/issues/591
    Input Text  id=${filter_items}  ${my_news_folder}
    # Acontece que, ao usar o filtro, o "Drag And Drop" acaba sendo executado
    # ANTES do "Input Text" ter um retorno na tela, ou seja, ele é executado com
    # o scroll "ainda ativo": por isso preciso desse "Sleep" logo abaixo para
    # "forçar" que o "Drag And Drop" só seja executado após o "Input Text".
    Sleep  1s
    Drag And Drop  xpath=${my_news_folder_selector}  css=${tile_selector}
    Wait Until Page Contains Element  css=div.mediacarousel.tile-content h2.mediacarousel-tile+div
    Wait Until Page Contains  ${title_nitf_with_image}
    Page Should Not Contain  ${title_nitf_without_image}

    # move to the default view and check tile persisted
    Click Link  link=View
    Page Should Contain Element  css=div.mediacarousel.tile-content h2.mediacarousel-tile

    # delete the tile
    Open Layout Tab
    Delete Tile
    Save Cover Layout
