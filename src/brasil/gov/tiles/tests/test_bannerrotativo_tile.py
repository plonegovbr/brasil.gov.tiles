# -*- coding: utf-8 -*-

from collective.cover.testing import INTEGRATION_TESTING
from collective.cover.tiles.base import IPersistentCoverTile
from brasil.gov.tiles.tiles.banner_rotativo import BannerRotativoTile
from zope.component import getMultiAdapter
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject

import unittest


class BannerRotativoTileTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.name = u"brasil.gov.tiles.banner_rotativo"
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
        self.assertTrue(self.tile.is_configurable)
        self.assertTrue(self.tile.is_droppable)
        self.assertTrue(self.tile.is_editable)

    def test_tile_is_empty(self):
        self.assertTrue(self.tile.is_empty())
