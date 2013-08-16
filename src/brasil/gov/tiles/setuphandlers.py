# -*- coding: utf-8 -*-

from brasil.gov.tiles.config import PROJECTNAME
from Products.CMFCore.utils import getToolByName

import logging


def upgrade_to_1001(context, logger=None):
    """
    """
    if logger is None:
        # Called as upgrade step: define our own logger
        logger = logging.getLogger(PROJECTNAME)

    profile = 'profile-brasil.gov.tiles:upgrade_to_1001'
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile(profile)
