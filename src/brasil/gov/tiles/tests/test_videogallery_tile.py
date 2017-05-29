# -*- coding: utf-8 -*-
from brasil.gov.tiles.testing import INTEGRATION_TESTING
from brasil.gov.tiles.testing import TOTAL_VIDEOS
from brasil.gov.tiles.testing import VIDEO_PREFIX
from brasil.gov.tiles.tiles.videogallery import IVideoGalleryTile
from brasil.gov.tiles.tiles.videogallery import VideoGalleryTile
from collective.cover.tests.base import TestTileMixin
from plone.tiles.interfaces import ITileDataManager

import unittest


class VideoGalleryTileTestCase(TestTileMixin, unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        super(VideoGalleryTileTestCase, self).setUp()
        self.tile = VideoGalleryTile(self.cover, self.request)
        self.tile.__name__ = u'audiogallery'
        self.tile.id = u'audio gallery test'
        self.tile.subtitle = u'subtitle'
        data_mgr = ITileDataManager(self.tile)
        old_data = data_mgr.get()
        old_data['subtitle'] = 'subtitle'
        data_mgr.set(old_data)

    def test_accepted_content_types(self):
        self.assertEqual(self.tile.accepted_ct(), ['Collection', 'Folder'])

    def test_default_configuration(self):
        self.assertTrue(self.tile.is_configurable)
        self.assertTrue(self.tile.is_droppable)
        self.assertTrue(self.tile.is_editable)

    @unittest.expectedFailure  # FIXME: raises BrokenImplementation
    def test_interface(self):
        self.interface = IVideoGalleryTile
        self.klass = VideoGalleryTile
        super(VideoGalleryTileTestCase, self).test_interface()

    def test_populate_with_object(self):
        # verifica a renderizacao com uma imagem
        obj = self.portal['my-videos']
        self.tile.populate_with_object(obj)
        rendered = self.tile()
        for i in range(0, TOTAL_VIDEOS):
            self.assertIn('{0}_{1}'.format(VIDEO_PREFIX, i), rendered)
