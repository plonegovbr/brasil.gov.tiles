# -*- coding: utf-8 -*-
from brasil.gov.tiles.config import PROJECTNAME
from collective.cover.controlpanel import ICoverSettings
from plone import api

import logging


def conserta_tile_poll_duplicado(context):
    """Verifica se collective.polls está duplicado."""
    logger = logging.getLogger(PROJECTNAME)

    tiles = api.portal.get_registry_record('plone.app.tiles')
    if len(tiles) != len(set(tiles)):
        api.portal.set_registry_record('plone.app.tiles', list(set(tiles)))

    record = dict(interface=ICoverSettings, name='available_tiles')
    available_tiles = api.portal.get_registry_record(**record)
    if len(available_tiles) != len(set(available_tiles)):
        api.portal.set_registry_record(value=list(set(available_tiles)), **record)

    logger.info('collective.polls duplicado verificado')
