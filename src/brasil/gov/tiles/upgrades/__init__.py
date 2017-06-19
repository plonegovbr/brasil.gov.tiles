# -*- coding: utf-8 -*-
from brasil.gov.tiles.config import PROJECTNAME
from plone import api

import logging


logger = logging.getLogger(PROJECTNAME)


def cook_javascript_resources(context):
    api.portal.get_tool('portal_javascripts').cookResources()
    logger.info('Javascript resources were cooked')
