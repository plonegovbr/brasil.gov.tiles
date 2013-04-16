# -*- coding: utf-8 -*-

from beyondskins.cartacapital.portal.config import PROJECTNAME
from beyondskins.cartacapital.portal.testing import INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.browserlayer.utils import registered_layers
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import unittest2 as unittest


TILES = [
    'nitf.basic',
    'poll',
]


class InstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']

    def test_browserlayer(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertIn('IBrasilGovTiles', layers, 'browser layer not installed')

    def test_tiles(self):
        self.registry = getUtility(IRegistry)
        registered_tiles = self.registry['plone.app.tiles']
        for tile in TILES:
            self.assertIn(tile, registered_tiles)


class UninstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME),
                         '%s not uninstalled' % PROJECTNAME)

    def test_browserlayer_removed(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertNotIn('IBrasilGovTiles', layers,
                         'browser layer not removed')
