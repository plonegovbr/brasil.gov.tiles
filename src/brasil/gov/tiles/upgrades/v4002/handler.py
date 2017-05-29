# -*- coding: utf-8 -*-
from brasil.gov.tiles.upgrades import logger
from plone.app.uuid.utils import uuidToObject
from plone.tiles.interfaces import ITileDataManager

TILE_TYPES = ['audiogallery', 'videogallery', 'mediacarousel']


def upgrades_tile_header_tile_title(context):
    """
    Novos campos adicionados/migrados apos herdar ListTile de collective.cover:

    header passa a ser tile_title;
    """
    covers = context.portal_catalog(portal_type='collective.cover.content')
    logger.info('{0} objetos capa a atualizar'.format(len(covers)))
    for cover in covers:
        obj = cover.getObject()
        tile_ids = obj.list_tiles(types=TILE_TYPES)
        msg = '{0} tiles do tipo {1} a atualizar para {2}'
        logger.info(msg.format(len(tile_ids), ', '.join(TILE_TYPES), cover.id))
        for tile_id in tile_ids:
            tile = obj.get_tile(tile_id)
            old_data = ITileDataManager(tile).get()

            header = old_data.get('header', '')
            if header:
                old_data['tile_title'] = header
                msg = '{0} atualizou o campo header'
                logger.info(msg.format(tile_id))
                del old_data['header']

                ITileDataManager(tile).set(old_data)
                logger.info(
                    'Tile {0} do cover {1} atualizado'.format(
                        tile_id, cover.getPath()
                    )
                )

    logger.info('upgrades_tile_header_tile_title finalizado.')


def _get_uid_and_length(uuids):
    # Faço os testes caso o upgradeStep seja rodado mais de uma
    # vez pelo portal_setup.
    try:
        length = len(uuids.keys())
        uid = uuids.keys()[0]
    except AttributeError:
        length = len(uuids)
        uid = uuids[0]

    # Se não for 'str', é um método, ou seja, um ATFolder e então precisamos
    # executá-lo.
    if type(uid) not in [str, unicode]:
        uid = uid()

    return uid, length


def corrige_uuids_se_colecao_ou_folder_e_seta_footer_text(context):
    """
    Tiles afetados:

        audiogallery, videogallery e mediacarousel.

    Quando você associava uma coleção ou diretório num tile, ficava armazenado
    o uuid dessa coleção ou diretório e, pelo método 'get_elements' sendo
    chamado na template, o diretório/coleção era percorrido e se pegava todos
    os objetos.

        https://github.com/plonegovbr/brasil.gov.tiles/blob/7419efc721e133e694526fcecf9c24531faa64ab/src/brasil/gov/tiles/tiles/audiogallery.py#L68
        https://github.com/plonegovbr/brasil.gov.tiles/blob/7419efc721e133e694526fcecf9c24531faa64ab/src/brasil/gov/tiles/tiles/videogallery.py#L98
        https://github.com/plonegovbr/brasil.gov.tiles/blob/7419efc721e133e694526fcecf9c24531faa64ab/src/brasil/gov/tiles/tiles/mediacarousel.py#L93

    Acontece que, ao voltar a herdar do tipo lista do collective.cover, que já
    fornece um método 'results', esse método get_elements não é mais necessário
    mas precisamos migrar todos os tiles que ainda esperam essa lógica: ou seja
    preciso pegar os tiles afetados, pegar os uuids associados e, caso
    seja coleção ou diretório, pegar os uuids filhos e associar novamente
    ao tile.

    Essa lógica inclusive já era a utilizada pelo tile de list desse pacote
    através do uso de ICoverUIDsProvider, em populate_with_object: mas nos
    tiles que herdavam do lista esse método era sobrescrito e o atributo uuids
    armazenado de outra forma, como pode ser visto em

        https://github.com/plonegovbr/brasil.gov.tiles/blob/7419efc721e133e694526fcecf9c24531faa64ab/src/brasil/gov/tiles/tiles/audiogallery.py#L57
        https://github.com/plonegovbr/brasil.gov.tiles/blob/7419efc721e133e694526fcecf9c24531faa64ab/src/brasil/gov/tiles/tiles/videogallery.py#L82
        https://github.com/plonegovbr/brasil.gov.tiles/blob/7419efc721e133e694526fcecf9c24531faa64ab/src/brasil/gov/tiles/tiles/mediacarousel.py#L72

    """
    covers = context.portal_catalog(portal_type='collective.cover.content')
    logger.info('{0} objetos capa a atualizar'.format(len(covers)))
    for cover in covers:
        obj = cover.getObject()
        tile_ids = obj.list_tiles(types=TILE_TYPES)
        msg = '{0} tiles {1} a atualizar'
        logger.info(msg.format(len(tile_ids), ', '.join(TILE_TYPES)))
        for tile_id in tile_ids:
            tile = obj.get_tile(tile_id)
            data_mgr = ITileDataManager(tile)
            old_data = data_mgr.get()
            uuids = old_data.get('uuids', [])
            if uuids:

                uid, length = _get_uid_and_length(uuids)

                # Se tiver apenas um uuid, ou seja, característica de quando
                # o populate_with_object recebia o Folder ou Coleção
                if length == 1:
                    obj_from_uuid = uuidToObject(uid)
                    portal_type = obj_from_uuid.getPortalTypeName()

                    if portal_type == 'Collection':
                        new_uuids = [i.UID for i in obj_from_uuid.results()]
                    elif portal_type == 'Folder':
                        new_uuids = [
                            i.UID for i in obj_from_uuid.getFolderContents()
                        ]

                    if tile.__name__ == 'videogallery':
                        old_data['uuid_container'] = uid

                    old_data['footer_text'] = obj_from_uuid.absolute_url()
                    data_mgr.set(old_data)

                    msg = 'uuids a atualizar: {0}'
                    logger.info(msg.format(new_uuids))
                    tile.replace_with_uuids(new_uuids)

    msg = 'corrige_uuids_se_colecao_ou_folder_e_seta_footer_text finalizado.'
    logger.info(msg)
