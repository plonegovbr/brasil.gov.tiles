# -*- coding: utf-8 -*-
from brasil.gov.tiles.config import PROJECTNAME
from collective.cover.controlpanel import ICoverSettings
from collective.cover.interfaces import ICover
from plone import api

import json
import logging


OLD_TILE = u'poll'
NEW_TILE = u'collective.polls'


def _change_tile_type(layout, is_child=False):
    """Recursively change tile type."""
    if not is_child:
        layout = json.loads(layout)
    fixed_layout = []
    for row in layout:
        fixed_row = row.copy()
        old_type = fixed_row.get(u'tile-type', None)
        if old_type == OLD_TILE:
            fixed_row[u'tile-type'] = NEW_TILE
        if u'children' in fixed_row:
            fixed_row[u'children'] = _change_tile_type(fixed_row[u'children'], True)
        fixed_layout.append(fixed_row)
    if is_child:
        return fixed_layout
    else:
        fixed_layout = json.dumps(fixed_layout)
        return fixed_layout.decode('utf-8')


def replace_poll_tile(context):
    """Replace poll tile with the one in collective.polls."""
    logger = logging.getLogger(PROJECTNAME)
    tiles = api.portal.get_registry_record('plone.app.tiles')
    if OLD_TILE in tiles:
        tiles.remove(OLD_TILE)
        if NEW_TILE not in tiles:
            tiles.append(NEW_TILE)
        api.portal.set_registry_record('plone.app.tiles', tiles)
    record = dict(interface=ICoverSettings, name='available_tiles')
    available_tiles = api.portal.get_registry_record(**record)
    if OLD_TILE in available_tiles:
        available_tiles.remove(OLD_TILE)
        if NEW_TILE not in available_tiles:
            available_tiles.append(NEW_TILE)
        api.portal.set_registry_record(value=available_tiles, **record)
    results = api.content.find(object_provides=ICover.__identifier__)
    for brain in results:
        obj = brain.getObject()
        obj.cover_layout = _change_tile_type(obj.cover_layout)
    logger.info('collective.polls tile replaced the poll tile')
