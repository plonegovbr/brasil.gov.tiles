# -*- coding: utf-8 -*-

from brasil.gov.tiles.testing import BaseIntegrationTestCase
from brasil.gov.tiles.tiles.poll import PollTile
from collective.cover.tiles.base import IPersistentCoverTile
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject


class PollTileTestCase(BaseIntegrationTestCase):

    def setUp(self):
        super(PollTileTestCase, self).setUp()
        self.tile = self.portal.restrictedTraverse(
            '@@{0}/{1}'.format('poll', 'test-tile')
        )

    def test_interface(self):
        self.assertTrue(IPersistentCoverTile.implementedBy(PollTile))
        self.assertTrue(verifyClass(IPersistentCoverTile, PollTile))

        tile = PollTile(None, None)
        self.assertTrue(IPersistentCoverTile.providedBy(tile))
        self.assertTrue(verifyObject(IPersistentCoverTile, tile))

    def test_default_configuration(self):
        self.assertFalse(self.tile.is_configurable)
        self.assertTrue(self.tile.is_editable)
        self.assertTrue(self.tile.is_droppable)

    def test_accepted_content_types(self):
        self.assertListEqual(
            self.tile.accepted_ct(), ['collective.polls.poll'])
