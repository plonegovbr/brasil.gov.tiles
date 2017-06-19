# -*- coding: utf-8 -*-
from brasil.gov.tiles.config import PROJECTNAME
from plone.app.upgrade.utils import loadMigrationProfile

import logging


def apply_profile(context):
    """Apply upgrade profile"""
    logger = logging.getLogger(PROJECTNAME)
    profile = 'profile-brasil.gov.tiles.upgrades.v3000:default'
    loadMigrationProfile(context, profile)
    logger.info('Applied upgrade profile to version 3000')
