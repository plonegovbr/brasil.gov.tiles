# -*- coding: utf-8 -*-
from brasil.gov.tiles.testing import BaseIntegrationTestCase
from brasil.gov.tiles.tiles.groupcarousel import GroupCarouselTile
from collective.cover.tiles.base import IPersistentCoverTile
from mock import Mock
from plone import api
from plone.tiles.interfaces import ITileDataManager
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject


class CarouselTileTestCase(BaseIntegrationTestCase):

    def setUp(self):
        super(CarouselTileTestCase, self).setUp()
        self.tile = self.portal.restrictedTraverse(
            '@@{0}/{1}'.format('brasil.gov.tiles.groupcarousel', 'test-tile'))

    def test_interface(self):
        self.assertTrue(IPersistentCoverTile.implementedBy(GroupCarouselTile))
        self.assertTrue(verifyClass(IPersistentCoverTile, GroupCarouselTile))

        tile = GroupCarouselTile(None, None)
        self.assertTrue(IPersistentCoverTile.providedBy(tile))
        self.assertTrue(verifyObject(IPersistentCoverTile, tile))

    def test_default_configuration(self):
        self.assertFalse(self.tile.is_configurable)
        self.assertTrue(self.tile.is_editable)
        self.assertTrue(self.tile.is_droppable)

    def test_tile_is_empty(self):
        self.assertTrue(self.tile.is_empty())

    def test_crud(self):
        # we start with an empty tile
        self.assertTrue(self.tile.is_empty())

        # now we add a couple of objects to the list
        obj1 = self.portal['my-document']
        obj2 = self.portal['my-image']
        self.tile.populate_with_object(obj1)
        self.tile.populate_with_object(obj2)
        # tile's data attribute is cached; reinstantiate it
        self.tile = self.portal.restrictedTraverse(
            '@@{0}/{1}'.format('brasil.gov.tiles.groupcarousel', 'test-tile'))
        self.assertEqual(len(max(self.tile.results())), 2)
        self.assertIn(obj1, next(self.tile.results()))
        self.assertIn(obj2, next(self.tile.results()))

        # next, we replace the list of objects with a different one
        obj3 = self.portal['my-news-item']
        self.tile.replace_with_uuids([api.content.get_uuid(obj3)])
        # tile's data attribute is cached; reinstantiate it
        self.tile = self.portal.restrictedTraverse(
            '@@{0}/{1}'.format('brasil.gov.tiles.groupcarousel', 'test-tile'))
        self.assertNotIn(obj1, next(self.tile.results()))
        self.assertNotIn(obj2, next(self.tile.results()))
        self.assertIn(obj3, next(self.tile.results()))

        # We edit the tile to give it a title and a 'more...' link.
        data = self.tile.data
        data['tile_title'] = 'My title'
        data['more_link'] = api.content.get_uuid(obj2)
        data['more_link_text'] = 'Read much more...'
        data['switch_text'] = 'Test switch text'
        # Save the new data.
        data_mgr = ITileDataManager(self.tile)
        data_mgr.set(data)

        # tile's data attribute is cached; reinstantiate it
        self.tile = self.portal.restrictedTraverse(
            '@@{0}/{1}'.format('brasil.gov.tiles.groupcarousel', 'test-tile'))
        self.assertEqual(self.tile.tile_title, 'My title')
        self.assertEqual(
            self.tile.more_link,
            {'href': 'http://nohost/plone/my-image',
             'text': 'Read much more...'})

        # finally, we remove it from the list; the tile must be empty again
        self.tile.remove_item(obj3.UID())
        # tile's data attribute is cached; reinstantiate it
        self.tile = self.portal.restrictedTraverse(
            '@@{0}/{1}'.format('brasil.gov.tiles.groupcarousel', 'test-tile'))
        self.assertTrue(self.tile.is_empty())

    def test_render_empty(self):
        msg = 'Add up to 12 objects to the tile.'

        self.tile.is_compose_mode = Mock(return_value=True)
        self.assertIn(msg, self.tile())

        self.tile.is_compose_mode = Mock(return_value=False)
        self.assertNotIn(msg, self.tile())

    def test_thumbnail(self):
        # as a File does not have an image field, we should have no thumbnail
        obj = self.portal['my-file']
        self.assertFalse(self.tile.thumbnail(obj))

        # as an Image does have an image field, we should have a thumbnail
        obj = self.portal['my-image']
        thumbnail = self.tile.thumbnail(obj)
        self.assertIsNotNone(thumbnail)

    def test_title(self):
        obj = self.portal['my-image']
        self.tile.populate_with_object(obj)
        self.assertEqual(self.tile.get_title(obj), 'Test image')

    def test_description(self):
        obj = self.portal['my-image']
        self.tile.populate_with_object(obj)
        self.assertEqual(self.tile.get_description(obj), 'This image was created for testing purposes')

    def test_render_with_image(self):
        obj1 = self.portal['my-image']
        obj2 = self.portal['my-document']
        self.tile.populate_with_object(obj1)

        data = self.tile.data
        data['tile_title'] = 'Carousel title'
        data['tile_description'] = 'Carousel description'
        data['more_link'] = api.content.get_uuid(obj2)
        data['more_link_text'] = 'Read much more...'
        data_mgr = ITileDataManager(self.tile)
        data_mgr.set(data)

        rendered = self.tile()

        self.assertFalse(self.tile.is_empty())
        self.assertIn('<img ', rendered)
        self.assertIn('alt="This image was created for testing purposes"', rendered)
        self.assertIn('<h2>Carousel title</h2>', rendered)
        self.assertIn('<p>Carousel description</p>', rendered)
        self.assertIn('Read much more...', rendered)
        self.assertIn('<a href="http://nohost/plone/my-document"', rendered)
