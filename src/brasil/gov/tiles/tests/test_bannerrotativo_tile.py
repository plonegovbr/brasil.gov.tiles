# -*- coding: utf-8 -*-
from brasil.gov.tiles.testing import INTEGRATION_TESTING
from brasil.gov.tiles.tiles.banner_rotativo import BannerRotativoTile
from collective.cover.tiles.base import IPersistentCoverTile
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject

import unittest


class BannerRotativoTileTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.request = self.layer['request']
        self.name = u"banner_rotativo"
        self.cover = self.portal['frontpage']
        self.tile = getMultiAdapter((self.cover, self.request), name=self.name)
        self.tile = self.tile['test']

    def test_interface(self):
        self.assertTrue(IPersistentCoverTile.implementedBy(BannerRotativoTile))
        self.assertTrue(verifyClass(IPersistentCoverTile, BannerRotativoTile))

        tile = BannerRotativoTile(None, None)
        self.assertTrue(IPersistentCoverTile.providedBy(tile))
        self.assertTrue(verifyObject(IPersistentCoverTile, tile))

    def test_default_configuration(self):
        self.assertFalse(self.tile.is_configurable)
        self.assertTrue(self.tile.is_droppable)
        self.assertTrue(self.tile.is_editable)

    def test_tile_is_empty(self):
        self.assertTrue(self.tile.is_empty())
