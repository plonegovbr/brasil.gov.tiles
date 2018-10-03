# -*- coding: utf-8 -*-
from brasil.gov.tiles.logger import logger
from plone import api


SCRIPTS = [
    '++resource++brasil.gov.tiles/brasilgovtiles.js',
]
STYLES = [
    '++resource++brasil.gov.tiles/brasilgovtiles.css',
]


def deprecate_resource_registries(setup_tool):
    """Deprecate resource registries."""
    js_tool = api.portal.get_tool('portal_javascripts')
    for js in SCRIPTS:
        js_tool.unregisterResource(id=js)
        assert js not in js_tool.getResourceIds()  # nosec
    logger.info('Scripts removed')

    css_tool = api.portal.get_tool('portal_css')
    for css in STYLES:
        css_tool.unregisterResource(id=css)
        assert css not in css_tool.getResourceIds()  # nosec
    logger.info('Styles removed')
