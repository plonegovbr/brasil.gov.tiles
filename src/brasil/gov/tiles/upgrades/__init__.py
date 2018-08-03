# -*- coding:utf-8 -*-
from brasil.gov.tiles.logger import logger
from collective.cover.controlpanel import ICoverSettings
from plone import api


def cook_css_resources(context):  # pragma: no cover
    """Cook CSS resources."""
    css_tool = api.portal.get_tool('portal_css')
    css_tool.cookResources()
    logger.info('CSS resources were cooked')


def cook_javascript_resources(context):  # pragma: no cover
    """Cook JavaScripts resources."""
    js_tool = api.portal.get_tool('portal_javascripts')
    js_tool.cookResources()
    logger.info('JavaScripts resources were cooked')


def add_tile(tile):
    """Add Quote Tile."""
    record = dict(name='plone.app.tiles')
    registered_tiles = api.portal.get_registry_record(**record)
    if tile not in registered_tiles:
        registered_tiles.append(tile)
        api.portal.set_registry_record(value=registered_tiles, **record)

    record = dict(interface=ICoverSettings, name='available_tiles')
    available_tiles = api.portal.get_registry_record(**record)
    if tile not in available_tiles:
        available_tiles.append(tile)
        api.portal.set_registry_record(value=available_tiles, **record)

    logger.info('{0} tile registered and made available'.format(tile))
