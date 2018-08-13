# -*- coding: utf-8 -*-
from brasil.gov.tiles.testing import BaseIntegrationTestCase
from brasil.gov.tiles.tiles.navigation import NavigationTile
from collective.cover.tiles.base import IPersistentCoverTile
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject


class NavigationTileTestCase(BaseIntegrationTestCase):

    def setUp(self):
        super(NavigationTileTestCase, self).setUp()
        self.tile = self.portal.restrictedTraverse(
            '@@{0}/{1}'.format('brasil.gov.tiles.navigation', 'test-tile'))

    def test_interface(self):
        self.assertTrue(IPersistentCoverTile.implementedBy(NavigationTile))
        self.assertTrue(verifyClass(IPersistentCoverTile, NavigationTile))

        tile = NavigationTile(None, None)
        self.assertTrue(IPersistentCoverTile.providedBy(tile))
        self.assertTrue(verifyObject(IPersistentCoverTile, tile))

    def test_default_configuration(self):
        self.assertFalse(self.tile.is_configurable)
        self.assertFalse(self.tile.is_editable)
        self.assertFalse(self.tile.is_droppable)

    def test_render_with_image(self):
        rendered = self.tile()
        self.assertIn('<ul class="navigation-items">', rendered)
        self.assertIn('<a href="http://nohost/plone/my-link">Test link</a>', rendered)

        tile = self.portal['my-news-folder'].restrictedTraverse(
            '@@{0}/{1}'.format('brasil.gov.tiles.navigation', 'test-tile'))

        rendered = tile()
        self.assertIn('<h2 class="navigation-title">Plone site</h2>', rendered)
        self.assertNotIn('<a href="http://nohost/plone/my-link">Test link</a>', rendered)
