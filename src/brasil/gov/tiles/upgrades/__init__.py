# -*- coding:utf-8 -*-
from brasil.gov.tiles.logger import logger
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
    from brasil.gov.tiles.utils import enable_tile
    enable_tile(tile)
    logger.info('{0} tile added'.format(tile))


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
    """Replace tile type on a layout."""
    new_layout = []
    for e in layout:
        if e.get('tile-type') == old:
            e['tile-type'] = new
        if e['type'] in ('row', 'group'):
            if 'children' in e:
                e['children'] = replace_tile(e['children'], old, new)
        new_layout.append(e)
    return new_layout


def remove_tile(layout, tile_type):
    """Remove tile type from a layout."""
    new_layout = []
    for e in layout:
        if e.get('tile-type') == tile_type:
            continue  # don't add the tile to the new layout
        if e['type'] in ('row', 'group'):
            if 'children' in e:
                e['children'] = remove_tile(e['children'], tile_type)
        new_layout.append(e)
    return new_layout


def replace_attribute(obj, tile_type, old, new):
    """Replace attribute on tiles."""
    if tile_type is None:
        return

    from plone.tiles.interfaces import ITileDataManager
    for id_ in obj.list_tiles(tile_type):
        tile = obj.get_tile(id_)
        data_mgr = ITileDataManager(tile)
        data = data_mgr.get()
        if data.get(old):
            data[new] = data.pop(old)
            data_mgr.set(data)
