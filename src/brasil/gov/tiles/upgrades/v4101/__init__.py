# -*- coding: utf-8 -*-
from brasil.gov.tiles.logger import logger
from plone import api


JS = '++resource++brasil.gov.tiles/brasilgovtiles.js'
CSS = '++resource++brasil.gov.tiles/brasilgovtiles.css'


def deprecate_resource_registries(setup_tool):
    """Deprecate resource registries."""
    js_tool = api.portal.get_tool('portal_javascripts')
    if JS in js_tool.getResourceIds():
        js_tool.unregisterResource(id=JS)
    assert JS not in js_tool.getResourceIds()  # nosec

    css_tool = api.portal.get_tool('portal_css')
    if CSS in css_tool.getResourceIds():
        css_tool.unregisterResource(id=CSS)
    assert CSS not in css_tool.getResourceIds()  # nosec

    logger.info('Static resources successfully removed from registries')
