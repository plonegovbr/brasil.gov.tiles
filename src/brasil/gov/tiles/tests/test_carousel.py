# -*- coding: utf-8 -*-
from brasil.gov.tiles.testing import INTEGRATION_TESTING
from brasil.gov.tiles.tiles.carousel import CarouselTile
from collective.cover.tiles.base import IPersistentCoverTile
from plone.app.imaging.interfaces import IImageScale
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from zope.component import getMultiAdapter
from zope.interface.verify import verifyClass

import unittest


class CarouselTileTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.request = self.layer['request']
        self.name = u'collective.cover.carousel'
        self.cover = self.portal['frontpage']
        self.tile = getMultiAdapter((self.cover, self.request), name=self.name)
        self.tile = self.tile['test']

    # @unittest.expectedFailure  # FIXME: raises BrokenImplementation
    def test_interface(self):
        self.assertTrue(IPersistentCoverTile.implementedBy(CarouselTile))
        self.assertTrue(verifyClass(IPersistentCoverTile, CarouselTile))

    def test_default_configuration(self):
        self.assertTrue(self.tile.is_configurable)
        self.assertTrue(self.tile.is_droppable)
        self.assertTrue(self.tile.is_editable)

    def test_tile_is_empty(self):
        self.assertTrue(self.tile.is_empty())

    def test_folder_tile_render(self):
        obj = self.portal['my-folder']
        self.tile.populate_with_object(obj)

        rendered = self.tile()
        msg = u'Galleria.loadTheme("++resource++collective.cover/galleria-theme/galleria.cover_theme.js");'
        self.assertIn(msg, rendered)

    def test_thumbnail(self):
        # as a File does not have an image field, we should have no thumbnail
        obj = self.portal['my-file']
        self.assertFalse(self.tile.thumbnail(obj))

        # as an Image does have an image field, we should have a thumbnail
        obj = self.portal['my-image']
        thumbnail = self.tile.thumbnail(obj)
        self.assertTrue(thumbnail)
        # the thumbnail is an ImageScale
        self.assertTrue(IImageScale.providedBy(thumbnail))
        tile_conf = self.tile.get_tile_configuration()
        tile_conf['image']['visibility'] = u'on'
        self.tile.set_tile_configuration(tile_conf)
        self.assertTrue(self.tile._field_is_visible('image'))
        self.assertTrue(self.tile.thumbnail(obj))
