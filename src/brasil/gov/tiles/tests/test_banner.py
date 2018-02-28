# -*- coding: utf-8 -*-
from brasil.gov.tiles.testing import BaseIntegrationTestCase
from brasil.gov.tiles.tiles.banner import BannerTile
from collective.cover.tiles.base import IPersistentCoverTile
from zope.interface.verify import verifyClass


class BannerTileTestCase(BaseIntegrationTestCase):

    def setUp(self):
        super(BannerTileTestCase, self).setUp()
        self.tile = self.portal.restrictedTraverse(
            '{0}/{1}'.format('collective.cover.banner', 'test-tile'),
        )

    def test_interface(self):
        self.assertTrue(IPersistentCoverTile.implementedBy(BannerTile))
        self.assertTrue(verifyClass(IPersistentCoverTile, BannerTile))

        tile = BannerTile(None, None)
        self.assertTrue(IPersistentCoverTile.providedBy(tile))

    def test_default_configuration(self):
        self.assertTrue(self.tile.is_configurable)
        self.assertTrue(self.tile.is_droppable)
        self.assertTrue(self.tile.is_editable)

    def test_accepted_content_types(self):
        self.assertEqual(self.tile.accepted_ct(), ['Image', 'Link'])

    def test_render_empty(self):
        rendered = self.tile()
        msg = u'Drag&amp;drop an image or link here to populate the tile.'
        self.assertIn(msg, rendered)

    def test_render_with_image(self):
        obj = self.portal['my-image']
        self.tile.populate_with_object(obj)
        rendered = self.tile()
        self.assertIn('<img ', rendered)
        self.assertIn('alt="This image was created for testing purposes"', rendered)
        self.assertTrue(self.tile.has_image)

    def test_render_with_link(self):
        obj = self.portal['my-link']
        self.tile.populate_with_object(obj)
        rendered = self.tile()
        self.assertNotIn('<img ', rendered)
        self.assertIn('">Test link</a>', rendered)
        self.assertFalse(self.tile.has_image)

    def test_title(self):
        obj = self.portal['my-image']
        self.tile.populate_with_object(obj)
        self.assertEqual(self.tile.Title(), 'Test image')
