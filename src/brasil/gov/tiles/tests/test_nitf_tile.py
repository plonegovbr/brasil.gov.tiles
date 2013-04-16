# -*- coding: utf-8 -*-

from brasil.gov.tiles.testing import BaseIntegrationTestCase
from brasil.gov.tiles.tiles.nitf import NITFBasicTile
from collective.cover.tiles.base import IPersistentCoverTile
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject

import unittest

# XXX: remove this when release available
import pkg_resources
nitf_available = 'collective.nitf' in pkg_resources.AvailableDistributions()
msg = "collective.nitf not installed; skipping test"


class NITFBasicTileTestCase(BaseIntegrationTestCase):

    def setUp(self):
        super(NITFBasicTileTestCase, self).setUp()
        self.tile = self.portal.restrictedTraverse(
            '@@%s/%s' % ('nitf.basic', 'test-tile'))

    @unittest.skipUnless(nitf_available, msg)
    def test_interface(self):
        self.assertTrue(IPersistentCoverTile.implementedBy(NITFBasicTile))
        self.assertTrue(verifyClass(IPersistentCoverTile, NITFBasicTile))

        tile = NITFBasicTile(None, None)
        self.assertTrue(IPersistentCoverTile.providedBy(tile))
        self.assertTrue(verifyObject(IPersistentCoverTile, tile))

    @unittest.skipUnless(nitf_available, msg)
    def test_default_configuration(self):
        self.assertTrue(self.tile.is_configurable)
        self.assertTrue(self.tile.is_editable)
        self.assertTrue(self.tile.is_droppable)

    @unittest.skipUnless(nitf_available, msg)
    def test_accepted_content_types(self):
        self.assertListEqual(
            self.tile.accepted_ct(), ['collective.nitf.content'])
