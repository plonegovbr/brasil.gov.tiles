# -*- coding: utf-8 -*-
from brasil.gov.tiles.testing import INTEGRATION_TESTING
from brasil.gov.tiles.tiles.audiogallery import AudioGalleryTile
from brasil.gov.tiles.tiles.audiogallery import IAudioGalleryTile
from collective.cover.tests.base import TestTileMixin

import unittest


class AudioGalleryTileTestCase(TestTileMixin, unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        super(AudioGalleryTileTestCase, self).setUp()
        self.tile = AudioGalleryTile(self.cover, self.request)
        self.tile.__name__ = u'audiogallery'
        self.tile.id = u'audio gallery test'

    def test_accepted_content_types(self):
        self.assertEqual(self.tile.accepted_ct(), ['Collection', 'Folder'])

    def test_default_configuration(self):
        self.assertTrue(self.tile.is_configurable)
        self.assertTrue(self.tile.is_droppable)
        self.assertTrue(self.tile.is_editable)

    @unittest.expectedFailure  # FIXME: raises BrokenImplementation
    def test_interface(self):
        self.interface = IAudioGalleryTile
        self.klass = AudioGalleryTile
        super(AudioGalleryTileTestCase, self).test_interface()

    def test_populate_with_object(self):
        # verifica a renderizacao com uma imagem
        obj = self.portal['my-audios']
        self.tile.populate_with_object(obj)
        rendered = self.tile()
        msgs = ['my-audios', 'my-audio', 'my-audio1', 'my-audio2']
        for msg in msgs:
            self.assertIn(msg, rendered)
