*** Settings ***

Resource  collective/cover/tests/cover.robot
Library  Remote  ${PLONE_URL}/RobotRemote

Suite Setup  Open Test Browser
Suite Teardown  Close all browsers

*** Variables ***

${filter_items}  contentchooser-content-trees
${my_videos}  my-videos
${videogallery_tile_location}  'videogallery'
${folder_selector}  .ui-draggable .contenttype-folder
${tile_selector}  div.tile-container div.tile

*** Test cases ***

Test Videogallery Tile
    Enable Autologin as  Site Administrator
    Go to Homepage
    Create Cover  Title  Description  Empty layout

    # add a videogallery tile to the layout
    Open Layout Tab
    Wait until page contains  Export layout
    Add Tile  ${videogallery_tile_location}
    Save Cover Layout

    # as tile is empty, we see default message
    Compose Cover
    Page Should Contain  Video Gallery

    # drag&drop a Video Folder
    Open Content Chooser
    Click Link  link=Content tree
    # Temos um bug no robots onde ele não consegue selecionar um ícone do overlay
    # "Adicionar conteúdo" se for necessário usar o scroll, era como se ele não
    # conseguisse "ver" o objeto: dessa forma, uso o filtro de items para mostrar
    # menos itens e evitar esse problema.
    # FIXME: https://github.com/robotframework/Selenium2Library/issues/591
    Input Text  id=${filter_items}  ${my_videos}
    # Acontece que, ao usar o filtro, o "Click" acaba sendo executado
    # ANTES do "Input Text" ter um retorno na tela, ou seja, ele é executado com
    # o scroll "ainda ativo": por isso preciso desse "Sleep" logo abaixo para
    # "forçar" que o "Click" só seja executado após o "Input Text".
    Sleep  1s
    Drag And Drop  css=${folder_selector}  css=${tile_selector}
    Wait Until Page Contains Element  css=div.videogallery-tile div.videogallery-inner div.player-holder div.player-video iframe

    # move to the default view and check tile persisted
    Click Link  link=View
    Page Should Contain Element  css=div.videogallery-tile div.videogallery-inner div.player-holder div.player-video iframe
    Page Should Contain Element  css=div.videogallery-tile div.galery-items div.galery-items-wrapper div.gallery-element div.gallery-element-wrapper a img

    # delete the tile
    Open Layout Tab
    Delete Tile
    Save Cover Layout
