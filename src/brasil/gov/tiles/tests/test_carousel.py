# -*- coding: utf-8 -*-
from brasil.gov.tiles.testing import INTEGRATION_TESTING
from brasil.gov.tiles.tiles.carousel import CarouselTile
from brasil.gov.tiles.tiles.carousel import ICarouselTile
from collective.cover.controlpanel import ICoverSettings
from collective.cover.tests.base import TestTileMixin
from plone.app.imaging.interfaces import IImageScale
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import unittest


class CarouselTileTestCase(TestTileMixin, unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        super(CarouselTileTestCase, self).setUp()
        self.tile = CarouselTile(self.cover, self.request)
        self.tile.__name__ = u'collective.cover.carousel'
        self.tile.id = u'test'

    @unittest.expectedFailure  # FIXME: raises BrokenImplementation
    def test_interface(self):
        self.interface = ICarouselTile
        self.klass = CarouselTile
        super(CarouselTileTestCase, self).test_interface()

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

    def test_accepted_content_types(self):
        # Using the same from ListTile since CarouselTile(ListTile)
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ICoverSettings)
        self.assertEqual(
            self.tile.accepted_ct(),
            settings.searchable_content_types
        )

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
