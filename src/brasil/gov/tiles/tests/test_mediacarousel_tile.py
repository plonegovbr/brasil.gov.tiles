# -*- coding: utf-8 -*-
from brasil.gov.tiles.testing import INTEGRATION_TESTING
from brasil.gov.tiles.tiles.mediacarousel import IMediaCarouselTile
from brasil.gov.tiles.tiles.mediacarousel import MediaCarouselTile
from collective.cover.tests.base import TestTileMixin
from mock import Mock
from plone import api
from plone.app.imaging.interfaces import IImageScale
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from zope.component import getMultiAdapter

import unittest


class MediaCarouselTileTestCase(TestTileMixin, unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        super(MediaCarouselTileTestCase, self).setUp()
        self.tile = MediaCarouselTile(self.cover, self.request)
        self.tile.__name__ = u'mediacarousel'
        self.tile.id = u'test'

    @unittest.expectedFailure  # FIXME: raises BrokenImplementation
    def test_interface(self):
        self.interface = IMediaCarouselTile
        self.klass = MediaCarouselTile
        super(MediaCarouselTileTestCase, self).test_interface()

    def test_default_configuration(self):
        self.assertTrue(self.tile.is_configurable)
        self.assertTrue(self.tile.is_droppable)
        self.assertTrue(self.tile.is_editable)

    def test_tile_is_empty(self):
        self.assertTrue(self.tile.is_empty())

    def test_accepted_content_types(self):
        self.assertEqual(self.tile.accepted_ct(), ['Collection', 'Folder'])

    def test_folder_tile_render(self):
        obj = self.portal['my-folder']
        self.tile.populate_with_object(obj)

        rendered = self.tile()
        msg = u'Drag a folder or collection to populate the tile.'
        self.assertIn(msg, rendered)

    def test_delete_folder(self):
        obj = self.portal['my-folder']
        self.tile.populate_with_object(obj)
        self.tile.populate_with_object(obj)

        rendered = self.tile()
        msg = u'Drag a folder or collection to populate the tile.'
        self.assertIn(msg, rendered)

        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Editor', 'Reviewer'])
        login(self.portal, TEST_USER_NAME)
        api.content.delete(obj=self.portal['my-folder'])

        rendered = self.tile()
        self.tile.is_compose_mode = Mock(return_value=True)
        self.assertIn(msg, rendered)

        self.tile.is_compose_mode = Mock(return_value=False)
        self.assertIn(msg, self.tile())

    def test_collection_tile_render(self):
        obj = self.portal['mandelbrot-set']
        self.tile.populate_with_object(obj)

        rendered = self.tile()
        msg = u'Mandelbrot set'
        self.assertIn(msg, rendered)

    def test_delete_collection(self):
        obj = self.portal['mandelbrot-set']
        self.tile.populate_with_object(obj)
        self.tile.populate_with_object(obj)

        rendered = self.tile()
        msg = u'Mandelbrot set'
        self.assertIn(msg, rendered)

        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Editor', 'Reviewer'])
        login(self.portal, TEST_USER_NAME)
        api.content.delete(obj=self.portal['mandelbrot-set'])

        msg = u'Drag a folder or collection to populate the tile.'

        rendered = self.tile()
        self.tile.is_compose_mode = Mock(return_value=True)
        self.assertIn(msg, rendered)

        self.tile.is_compose_mode = Mock(return_value=False)
        self.assertIn(msg, self.tile())

    def test_thumbnail(self):
        # as a File does not have an image field, we should have no thumbnail
        obj = self.portal['my-file']
        self.assertFalse(self.tile.thumbnail(obj))

        # nitf with Image, we should have a thumbnail
        obj = self.portal['my-news-folder']['my-nitf-with-image']
        [image_child] = [i for i in api.content.find(context=obj,
                         depth=1, portal_type='Image')]
        thumbnail = self.tile.thumbnail(image_child.getObject())  # noqa: E501; pylint: disable=W1662
        self.assertTrue(thumbnail)
        # the thumbnail is an ImageScale
        self.assertTrue(IImageScale.providedBy(thumbnail))

        # nitf without Image, we shouldn't have a thumbnail
        obj = self.portal['my-news-folder']['my-nitf-without-image']
        [image_child] = [i for i in api.content.find(context=obj,  # noqa: E501; pylint: disable=W1662
                         depth=1, portal_type='Image')] or [None]
        thumbnail = self.tile.thumbnail(image_child)  # noqa: E501; pylint: disable=W1662
        self.assertFalse(thumbnail)
        # the thumbnail is an ImageScale
        self.assertFalse(IImageScale.providedBy(thumbnail))

        # as an Image does have an image field, we should have a thumbnail
        obj = self.portal['my-image']
        thumbnail = self.tile.thumbnail(obj)
        self.assertTrue(thumbnail)
        # the thumbnail is an ImageScale
        self.assertTrue(IImageScale.providedBy(thumbnail))

        # turn visibility off, we should have no thumbnail
        # XXX: refactor; we need a method to easily change field visibility
        tile_conf = self.tile.get_tile_configuration()
        tile_conf['image']['visibility'] = u'off'
        self.tile.set_tile_configuration(tile_conf)

        self.assertFalse(self.tile._field_is_visible('image'))
        self.assertTrue(self.tile.thumbnail(obj))

        # TODO: test against Dexterity-based content types

    def test_crud_nitf(self):
        # we start with an empty tile
        self.assertTrue(self.tile.is_empty())

        # now we add a couple of nitf objects in a folder to the carousel
        obj1 = self.portal['my-news-folder']
        self.tile.populate_with_object(obj1)

        # tile's data attributed is cached so we should re-instantiate the tile
        tile = getMultiAdapter(
            (self.cover, self.request),
            name=self.tile.__name__,
        )
        tile = tile['test']

        self.assertEqual(len(tile.data['uuids']), 1)
        self.assertTrue(obj1 in tile.results())

        # finally, we remove it from the carousel; the tile must be empty again
        tile.remove_item(obj1.UID())
        # tile's data attributed is cached so we should re-instantiate the tile
        tile = getMultiAdapter(
            (self.cover, self.request),
            name=self.tile.__name__,
        )
        tile = tile['test']
        self.assertTrue(tile.is_empty())
