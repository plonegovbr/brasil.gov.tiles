# -*- coding: utf-8 -*-

from brasil.gov.tiles.testing import BaseIntegrationTestCase
from brasil.gov.tiles.tiles.social import SocialTile
from collective.cover.tiles.base import IPersistentCoverTile
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject


class SocialTileTestCase(BaseIntegrationTestCase):

    def setUp(self):
        super(SocialTileTestCase, self).setUp()
        self.tile = self.portal.restrictedTraverse(
            '@@{0}/{1}'.format('social', 'test-tile'))

    def test_interface(self):
        self.assertTrue(IPersistentCoverTile.implementedBy(SocialTile))
        self.assertTrue(verifyClass(IPersistentCoverTile, SocialTile))

        tile = SocialTile(None, None)
        self.assertTrue(IPersistentCoverTile.providedBy(tile))
        self.assertTrue(verifyObject(IPersistentCoverTile, tile))

    def test_render(self):
        self.tile.data['wid'] = '000000000000000000'
        self.tile.data['username'] = 'Portal Brasil'
        self.tile.data['facebook_page'] = 'https://www.facebook.com/'
        rendered = self.tile()
        self.assertIn('<ul class="social-tabs css-tabs">', rendered)
        self.assertIn('<li>Facebook</li>', rendered)
        self.assertIn('<li>Twitter</li>', rendered)
