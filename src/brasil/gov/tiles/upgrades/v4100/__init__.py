# -*- coding: utf-8 -*-
from brasil.gov.tiles.logger import logger
from brasil.gov.tiles.upgrades import add_tile
from plone import api


RESOURCES_TO_UPDATE = {
    '++resource++brasil.gov.tiles/tiles.css': '++resource++brasil.gov.tiles/brasilgovtiles.css',
    '++resource++brasil.gov.tiles/vendor/swiper.min.css': '++resource++brasil.gov.tiles/vendor/swiper.min.css',
    '++resource++brasil.gov.tiles/tiles.js': '++resource++brasil.gov.tiles/brasilgovtiles.js',
    '++resource++brasil.gov.tiles/jquery.cycle2.carousel.js': '++resource++brasil.gov.tiles/vendor/jquery.cycle2.carousel.js',
    '++resource++brasil.gov.tiles/jquery.cycle2.js': '++resource++brasil.gov.tiles/vendor/jquery.cycle2.js',
    '++resource++brasil.gov.tiles/jquery.jplayer.min.js': '++resource++brasil.gov.tiles/vendor/jquery.jplayer.min.js',
    '++resource++brasil.gov.tiles/vendor/swiper.min.js': '++resource++brasil.gov.tiles/vendor/vendor/swiper.min.js',
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


def add_quote_tile(setup_tool):
    """Add Quote tile."""
    add_tile(u'brasil.gov.tiles.quote')


def add_potd_tile(setup_tool):
    """Add Photo of the Day tile."""
    add_tile(u'brasil.gov.tiles.potd')


def add_photogallery_tile(setup_tool):
    """Add Photo Gallery tile."""
    add_tile(u'brasil.gov.tiles.photogallery')
