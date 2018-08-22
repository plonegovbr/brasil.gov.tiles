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
    """Register a tile and make it available."""
    name = 'plone.app.tiles'
    registered_tiles = api.portal.get_registry_record(name=name)
    if tile not in registered_tiles:
        registered_tiles.append(tile)
        api.portal.set_registry_record(name=name, value=registered_tiles)
        logger.info('{0} tile registered'.format(tile))

    record = dict(interface=ICoverSettings, name='available_tiles')
    available_tiles = api.portal.get_registry_record(**record)
    if tile not in available_tiles:
        available_tiles.append(tile)
        api.portal.set_registry_record(value=available_tiles, **record)
        logger.info('{0} tile made available'.format(tile))


def get_valid_objects(**kw):
    """Generate a list of objects associated with valid brains."""
    results = api.content.find(**kw)
    logger.info('Found {0} objects in the catalog'.format(len(results)))
    for b in results:
        try:
            obj = b.getObject()
        except (AttributeError, KeyError):
            obj = None

        if obj is None:  # warn on broken entries in the catalog
            msg = 'Invalid object reference in the catalog: {0}'
            logger.warn(msg.format(b.getPath()))
            continue

        yield obj


def replace_tile(layout, old, new):
    """Replace in layout old tile type with new one."""
    new_layout = []
    for e in layout:
        if 'tile-type' in e and e['tile-type'] == old:
            e['tile-type'] = new
        if e['type'] in ('row', 'group'):
            e['children'] = replace_tile(e['children'], old, new)
        new_layout.append(e)
    return new_layout
