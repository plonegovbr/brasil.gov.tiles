# -*- coding: utf-8 -*-
from collective.cover.controlpanel import ICoverSettings
from plone import api


# TODO: remove all code related to tile registration as registry
#       record is deprecated (we are using plone.app.tiles > 3.0.0)
#       see: https://github.com/plone/plone.app.tiles/pull/14
def get_registered_tiles():
    """Return a list of registered tiles."""
    return api.portal.get_registry_record(name='plone.app.tiles')


def set_registered_tiles(value):
    """Set a list of registered tiles."""
    api.portal.set_registry_record(value=value, name='plone.app.tiles')


def get_available_tiles():
    """Return a list of available tiles."""
    record = dict(interface=ICoverSettings, name='available_tiles')
    return api.portal.get_registry_record(**record)


def set_available_tiles(value):
    """Set a list of available tiles."""
    record = dict(interface=ICoverSettings, name='available_tiles')
    api.portal.set_registry_record(value=value, **record)


def enable_tile(tile):
    """Register tile and enable it."""
    registered_tiles = get_registered_tiles()
    if tile not in registered_tiles:
        registered_tiles.append(tile)
        set_registered_tiles(value=registered_tiles)
        assert tile in get_registered_tiles()  # nosec
    available_tiles = get_available_tiles()
    if tile not in available_tiles:
        available_tiles.append(tile)
        set_available_tiles(value=available_tiles)
        assert tile in get_available_tiles()  # nosec


def disable_tile(tile):
    """Unregister tile and disable it."""
    registered_tiles = get_registered_tiles()
    if tile in registered_tiles:
        registered_tiles.remove(tile)
        set_registered_tiles(value=registered_tiles)
        assert tile not in get_registered_tiles()  # nosec
    available_tiles = get_available_tiles()
    if tile in available_tiles:
        available_tiles.remove(tile)
        set_available_tiles(value=available_tiles)
        assert tile not in get_available_tiles()  # nosec
