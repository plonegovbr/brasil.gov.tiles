# -*- coding: utf-8 -*-
from brasil.gov.tiles.testing import BaseIntegrationTestCase
from brasil.gov.tiles.tiles.photogallery import PhotoGalleryTile
from collective.cover.tiles.base import IPersistentCoverTile
from mock import Mock
from plone.tiles.interfaces import ITileDataManager
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject


class PhotoGalleryTileTestCase(BaseIntegrationTestCase):

    def setUp(self):
        super(PhotoGalleryTileTestCase, self).setUp()
        self.tile = self.portal.restrictedTraverse(
            '@@{0}/{1}'.format('brasil.gov.tiles.photogallery', 'test-tile'))

    def test_interface(self):
        self.assertTrue(IPersistentCoverTile.implementedBy(PhotoGalleryTile))
        self.assertTrue(verifyClass(IPersistentCoverTile, PhotoGalleryTile))

        tile = PhotoGalleryTile(None, None)
        self.assertTrue(IPersistentCoverTile.providedBy(tile))
        self.assertTrue(verifyObject(IPersistentCoverTile, tile))

    def test_default_configuration(self):
        self.assertTrue(self.tile.is_configurable)
        self.assertTrue(self.tile.is_editable)
        self.assertTrue(self.tile.is_droppable)

    def test_accepted_content_types(self):
        self.assertListEqual(self.tile.accepted_ct(), ['Image'])

    def test_tile_is_empty(self):
        self.assertTrue(self.tile.is_empty())

    def test_render_empty(self):
        msg = 'Drag&amp;drop an image here to populate the tile.'

        self.tile.is_compose_mode = Mock(return_value=True)
        self.assertIn(msg, self.tile())

        self.tile.is_compose_mode = Mock(return_value=False)
        self.assertNotIn(msg, self.tile())

    def test_crud(self):
        self.assertTrue(self.tile.is_empty())

        obj = self.portal['my-image']
        obj2 = self.portal['my-image1']
        obj3 = self.portal['my-image2']

        self.tile.populate_with_object(obj)
        self.tile.populate_with_object(obj2)
        self.tile.populate_with_object(obj3)

        self.tile = self.portal.restrictedTraverse(
            '@@{0}/{1}'.format('brasil.gov.tiles.photogallery', 'test-tile'))

        self.assertEqual(len(self.tile.results()), 3)
        self.assertIn(obj, self.tile.results())
        self.assertIn(obj2, self.tile.results())
        self.assertIn(obj3, self.tile.results())

        data = self.tile.data
        data['tile_title'] = 'My title'
        data_mgr = ITileDataManager(self.tile)
        data_mgr.set(data)

        self.tile = self.portal.restrictedTraverse(
            '@@{0}/{1}'.format('brasil.gov.tiles.photogallery', 'test-tile'))
        self.assertEqual(self.tile.tile_title, 'My title')

    def test_render_with_image(self):
        obj = self.portal['my-image']
        self.tile.populate_with_object(obj)
        rendered = self.tile()
        self.assertFalse(self.tile.is_empty())
        self.assertIn('<img ', rendered)
        self.assertIn('alt="This image was created for testing purposes"', rendered)

    def test_thumbnail(self):
        obj = self.portal['my-image']
        thumbnail = self.tile.thumbnail(obj)
        self.assertIsNotNone(thumbnail)
