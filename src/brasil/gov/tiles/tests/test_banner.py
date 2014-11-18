# -*- coding: utf-8 -*-
from brasil.gov.tiles.testing import INTEGRATION_TESTING
from brasil.gov.tiles.tiles.banner import BannerTile
from collective.cover.tiles.base import IPersistentCoverTile
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from zope.component import getMultiAdapter
from zope.interface.verify import verifyClass

import unittest


class BannerTileTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.request = self.layer['request']
        self.name = u'collective.cover.banner'
        self.cover = self.portal['frontpage']
        self.tile = getMultiAdapter((self.cover, self.request), name=self.name)
        self.tile = self.tile['test']

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
        self.assertEqual(self.tile.accepted_ct(), ['Collection', 'Document', 'File', 'Form Folder', 'Image', 'Link', 'News Item'])

    def test_render_empty(self):
        rendered = self.tile()
        msg = u'Drag&amp;drop an image or link here to populate the tile.'
        self.assertIn(msg, rendered)

    def test_render_with_image(self):
        obj = self.portal['my-image']
        self.tile.populate_with_object(obj)
        rendered = self.tile()
        self.assertIn('<img ', rendered)
        self.assertIn('alt="Test image"', rendered)
        self.assertTrue(self.tile.has_image)

    def test_render_with_link(self):
        obj = self.portal['my-link']
        self.tile.populate_with_object(obj)
        rendered = self.tile()
        self.assertNotIn('<img ', rendered)
        self.assertIn('<a href="http://">Test link</a>', rendered)
        self.assertFalse(self.tile.has_image)

    def test_title(self):
        obj = self.portal['my-image']
        self.tile.populate_with_object(obj)
        self.assertEqual(self.tile.Title(), 'Test image')

    def test_getRemoteUrl(self):
        obj = self.portal['my-image']
        self.tile.populate_with_object(obj)
        self.assertEqual(self.tile.getRemoteUrl(), '/plone/my-image/view')
