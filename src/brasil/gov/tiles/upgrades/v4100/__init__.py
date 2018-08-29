# -*- coding: utf-8 -*-
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

SWIPER_CSS = '++resource++brasil.gov.tiles/vendor/swiper.min.css'
SWIPER_JS = '++resource++brasil.gov.tiles/vendor/swiper.min.js'


def _rename_resources(tool, from_to):
    for id_ in tool.getResourceIds():
        if id_ in from_to:
            tool.renameResource(id_, from_to[id_])


def update_static_resources(setup_tool):
    """Fix resource references after static files reorganization."""
    css_tool = api.portal.get_tool('portal_css')
    _rename_resources(css_tool, RESOURCES_TO_UPDATE)
    css_tool.registerResource(SWIPER_CSS)

    logger.info('CSS resources were updated')

    js_tool = api.portal.get_tool('portal_javascripts')
    _rename_resources(js_tool, RESOURCES_TO_UPDATE)
    js_tool.registerResource(SWIPER_JS)
    logger.info('JavaScript resources were updated')


DEPRECATED_TILES = [
    u'em_destaque',
    u'mediacarousel',
    u'nitf',
]


def remove_deprecated_tiles(setup_tool):
    """Remove deprecated tiles."""
    from brasil.gov.tiles.utils import disable_tile
    for tile in DEPRECATED_TILES:
        disable_tile(tile)


NEW_TILES = [
    u'brasil.gov.tiles.quote',
    u'brasil.gov.tiles.potd',
    u'brasil.gov.tiles.photogallery',
    u'brasil.gov.tiles.navigation',
    u'brasil.gov.tiles.videocarousel',
    u'brasil.gov.tiles.groupcarousel',
]


def add_new_tiles(setup_tool):
    """Add new tiles."""
    for tile in NEW_TILES:
        add_tile(tile)


def replace_nitf_tile(setup_tool):
    """Replace NITF tile."""
    from brasil.gov.tiles.upgrades import replace_tile
    tile = u'collective.nitf'
    add_tile(tile)

    logger.info('Replacing NITF tile on collective.cover objects')
    for obj in get_valid_objects(portal_type='collective.cover.content'):
        try:
            layout = json.loads(obj.cover_layout)
        except TypeError:
            continue  # empty layout?

        layout = replace_tile(layout, 'nitf', tile)
        obj.cover_layout = json.dumps(layout)

        replace_attribute(obj, tile, 'image_description', 'alt_text')

    logger.info('Done')


def remove_em_destaque_tile(setup_tool):
    """Remove Em destaque tile.
    The tile is not used on IDG v2 and there's no substitute for it.
    """
    from brasil.gov.tiles.upgrades import remove_tile
    logger.info('Removing Em destaque tile from collective.cover objects')
    for obj in get_valid_objects(portal_type='collective.cover.content'):
        try:
            layout = json.loads(obj.cover_layout)
        except TypeError:
            continue  # empty layout?

        layout = remove_tile(layout, 'em_destaque')
        obj.cover_layout = json.dumps(layout)

    logger.info('Done')


def replace_mediacarousel_tile(setup_tool):
    """Replace Media Carousel tile."""
    # TODO


def update_banner_tile(setup_tool):
    """Update Banner tile."""
    tile = u'collective.cover.banner'

    logger.info('Updating NITF tile on collective.cover objects')
    for obj in get_valid_objects(portal_type='collective.cover.content'):
        replace_attribute(obj, tile, 'image_description', 'alt_text')

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
