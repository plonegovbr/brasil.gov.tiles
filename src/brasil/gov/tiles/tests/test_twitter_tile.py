# -*- coding: utf-8 -*-

from brasil.gov.tiles.testing import BaseIntegrationTestCase
from brasil.gov.tiles.tiles.twitter import TwitterTile
from collective.cover.tiles.base import IPersistentCoverTile
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject


class TwitterTileTestCase(BaseIntegrationTestCase):

    def setUp(self):
        super(TwitterTileTestCase, self).setUp()
        self.tile = self.portal.restrictedTraverse(
            '@@%s/%s' % ('twitter', 'twitter-tile'))

    def test_interface(self):
        self.assertTrue(IPersistentCoverTile.implementedBy(TwitterTile))
        self.assertTrue(verifyClass(IPersistentCoverTile, TwitterTile))

        tile = TwitterTile(None, None)
        self.assertTrue(IPersistentCoverTile.providedBy(tile))
        self.assertTrue(verifyObject(IPersistentCoverTile, tile))

    def test_default_configuration(self):
        self.assertFalse(self.tile.is_configurable)
        self.assertTrue(self.tile.is_editable)
        self.assertFalse(self.tile.is_droppable)

    def test_accepted_content_types(self):
        self.assertIsNone(self.tile.accepted_ct())

    def test_wid(self):
        self.tile.data['wid'] = 123456
        self.assertEqual(123456, self.tile.get_wid())

    def test_username(self):
        self.tile.data['username'] = 'portalbrasil'
        self.assertEqual('portalbrasil', self.tile.get_username())
