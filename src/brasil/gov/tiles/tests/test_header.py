# -*- coding: utf-8 -*-
from brasil.gov.tiles.testing import BaseIntegrationTestCase
from brasil.gov.tiles.tiles.header import HeaderTile
from collective.cover.controlpanel import ICoverSettings
from collective.cover.tiles.base import IPersistentCoverTile
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject


class HeaderTileTestCase(BaseIntegrationTestCase):

    def setUp(self):
        super(HeaderTileTestCase, self).setUp()
        self.tile = self.portal.restrictedTraverse(
            '@@%s/%s' % ('standaloneheader', 'test-tile'))

    def test_interface(self):
        self.assertTrue(IPersistentCoverTile.implementedBy(HeaderTile))
        self.assertTrue(verifyClass(IPersistentCoverTile, HeaderTile))
        tile = HeaderTile(None, None)
        self.assertTrue(IPersistentCoverTile.providedBy(tile))
        self.assertTrue(verifyObject(IPersistentCoverTile, tile))

    def test_default_configuration(self):
        self.assertTrue(self.tile.is_configurable)
        self.assertTrue(self.tile.is_droppable)
        self.assertTrue(self.tile.is_editable)

    def test_accepted_content_types(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ICoverSettings)
        self.assertEqual(
            self.tile.accepted_ct(),
            settings.searchable_content_types
        )

    def test_populate_with_object(self):

        obj = self.portal['my-news-item']
        self.tile.populate_with_object(obj)
        rendered = self.tile()

        # Checando por link no título
        self.assertIn(
            '<h2 class="outstanding-title"><a href="http://nohost/plone/my-' +
            'news-item">Test news item</a></h2>',
            rendered
        )
        self.assertIn(
            '<a class="outstanding-link" href="http://nohost/plone/my-news' +
            '-item"',
            rendered
        )
