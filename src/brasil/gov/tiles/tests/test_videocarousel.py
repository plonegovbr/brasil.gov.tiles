# -*- coding: utf-8 -*-
from brasil.gov.tiles.testing import BaseIntegrationTestCase
from brasil.gov.tiles.tiles.videocarousel import VideoCarouselTile
from collective.cover.tiles.base import IPersistentCoverTile
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject


class VideoCarouselTileTestCase(BaseIntegrationTestCase):

    def setUp(self):
        super(VideoCarouselTileTestCase, self).setUp()
        self.tile = self.portal.restrictedTraverse(
            '@@{0}/{1}'.format('brasil.gov.tiles.videocarousel', 'test-tile'))

    def test_interface(self):
        self.assertTrue(IPersistentCoverTile.implementedBy(VideoCarouselTile))
        self.assertTrue(verifyClass(IPersistentCoverTile, VideoCarouselTile))

        tile = VideoCarouselTile(None, None)
        self.assertTrue(IPersistentCoverTile.providedBy(tile))
        self.assertTrue(verifyObject(IPersistentCoverTile, tile))

    def test_default_configuration(self):
        self.assertTrue(self.tile.is_configurable)
        self.assertTrue(self.tile.is_editable)
        self.assertTrue(self.tile.is_droppable)

    def test_accepted_content_types(self):
        self.assertListEqual(
            self.tile.accepted_ct(), ['sc.embedder'])

    def test_render_with_video(self):
        obj = self.portal['multimedia']
        self.tile.populate_with_object(obj)
        rendered = self.tile()
        self.assertIn('<img ', rendered)
        self.assertIn('alt="multimedia"', rendered)
