# -*- coding: utf-8 -*-
from brasil.gov.tiles import utils
from brasil.gov.tiles.logger import logger
from brasil.gov.tiles.upgrades import add_tile
from brasil.gov.tiles.upgrades import get_valid_objects
from brasil.gov.tiles.upgrades import replace_attribute
from collective.cover.controlpanel import ICoverSettings
from plone import api

import json


RESOURCES_TO_UPDATE = {
    '++resource++brasil.gov.tiles/tiles.css': '++resource++brasil.gov.tiles/brasilgovtiles.css',
    '++resource++brasil.gov.tiles/tiles.js': '++resource++brasil.gov.tiles/brasilgovtiles.js',
    '++resource++brasil.gov.tiles/jquery.cycle2.carousel.js': '++resource++brasil.gov.tiles/vendor/jquery.cycle2.carousel.js',
    '++resource++brasil.gov.tiles/jquery.cycle2.js': '++resource++brasil.gov.tiles/vendor/jquery.cycle2.js',
    '++resource++brasil.gov.tiles/jquery.jplayer.min.js': '++resource++brasil.gov.tiles/vendor/jquery.jplayer.min.js',
}


def _rename_resources(tool, from_to):
    for id_ in tool.getResourceIds():
        if id_ in from_to:
            tool.renameResource(id_, from_to[id_])


def update_static_resources(setup_tool):
    """Fix resource references after static files reorganization."""
    css_tool = api.portal.get_tool('portal_css')
    _rename_resources(css_tool, RESOURCES_TO_UPDATE)

    logger.info('CSS resources were updated')

    js_tool = api.portal.get_tool('portal_javascripts')
    _rename_resources(js_tool, RESOURCES_TO_UPDATE)
    logger.info('JavaScript resources were updated')


# a list of tile tuples (deprecated, replacement)
# if replacement is None, the tile will be removed from layouts
# for collective.cover tiles we only need to update of the alt_text attribute
DEPRECATED_TILES = [
    (u'banner_rotativo', None),
    (u'collective.cover.banner', u'collective.cover.banner'),
    (u'collective.cover.basic', u'collective.cover.basic'),
    (u'destaque', None),
    (u'em_destaque', None),
    (u'mediacarousel', None),
    (u'nitf', u'collective.nitf'),
    (u'social', None),
]


def disable_deprecated_tiles(setup_tool):
    """Disable deprecated tiles."""
    deprecated, new = [], []
    for d, r in DEPRECATED_TILES:
        if r is None:  # deprecating
            deprecated.append(d)
            continue

        if d != r:  # replacing
            deprecated.append(d)
            new.append(r)

    registered_tiles = utils.get_registered_tiles()
    registered_tiles = list(
        (set(registered_tiles) - set(deprecated)) | set(new))
    utils.set_registered_tiles(value=registered_tiles)

    available_tiles = utils.get_available_tiles()
    available_tiles = list(
        (set(available_tiles) - set(deprecated)) | set(new))
    utils.set_available_tiles(value=available_tiles)

    for tile in deprecated:
        assert tile not in utils.get_registered_tiles()  # nosec
        assert tile not in utils.get_available_tiles()  # nosec

    for tile in new:
        assert tile in utils.get_registered_tiles()  # nosec
        assert tile in utils.get_available_tiles()  # nosec


NEW_TILES = [
    u'brasil.gov.tiles.quote',
    u'brasil.gov.tiles.potd',
    u'brasil.gov.tiles.photogallery',
    u'brasil.gov.tiles.navigation',
    u'brasil.gov.tiles.videocarousel',
    u'brasil.gov.tiles.groupcarousel',
    u'brasil.gov.tiles.highlightscarousel',
]


def add_new_tiles(setup_tool):
    """Add new tiles."""
    for tile in NEW_TILES:
        add_tile(tile)


def migrate_deprecated_tiles(setup_tool):
    """Migrate deprecated tiles.

    - tiles with a substitute will be migrated
    - tiles with no substitute will be removed
    """
    from brasil.gov.tiles.upgrades import remove_tile
    from brasil.gov.tiles.upgrades import replace_tile

    logger.info('Migrating IDG tiles on collective.cover objects')
    logger.warn('All tiles with no substitute will be removed from layouts')
    for obj in get_valid_objects(portal_type='collective.cover.content'):
        try:
            layout = json.loads(obj.cover_layout)
        except TypeError:
            continue  # empty layout?

        for old, new in DEPRECATED_TILES:
            if new is None:
                layout = remove_tile(layout, old)
            elif old != new:
                layout = replace_tile(layout, old, new)
            obj.cover_layout = json.dumps(layout)
            replace_attribute(obj, new, 'image_description', 'alt_text')

    logger.info('Done')


def install_embedder(setup_tool):
    """Install sc.embedder."""
    addon = 'sc.embedder'
    qi = api.portal.get_tool('portal_quickinstaller')
    if not qi.isProductInstalled(addon):
        qi.installProduct(addon)
        logger.info(addon + ' was installed')


def make_embedder_searchable(setup_tool):
    """Make Embedder searchable at collective.cover."""
    content_type = 'sc.embedder'
    record = dict(interface=ICoverSettings, name='searchable_content_types')
    searchable_content_types = api.portal.get_registry_record(**record)
    if content_type not in searchable_content_types:
        searchable_content_types.append(content_type)
        api.portal.set_registry_record(value=searchable_content_types, **record)
        logger.info(
            'Embedder was made searchable in collective.cover configlet')


def install_imagecropping_manager(setup_tool):
    """Install plone.app.imagecropping."""
    addon = 'plone.app.imagecropping'
    qi = api.portal.get_tool('portal_quickinstaller')
    if not qi.isProductInstalled(addon):
        qi.installProduct(addon)
        logger.info(addon + ' was installed')


def avoid_searchable_content_types_duplication(setup_tool):
    """Avoid searchable_content_types duplication."""
    content_types = utils.get_searchable_content_types()
    utils.set_searchable_content_types(content_types)
