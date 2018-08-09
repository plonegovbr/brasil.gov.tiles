# -*- coding: utf-8 -*-
from brasil.gov.tiles.testing import BaseIntegrationTestCase
from brasil.gov.tiles.tiles.potd import POTDTile
from collective.cover.tiles.base import IPersistentCoverTile
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject


class POTDTileTestCase(BaseIntegrationTestCase):

    def setUp(self):
        super(POTDTileTestCase, self).setUp()
        self.tile = self.portal.restrictedTraverse(
            '@@{0}/{1}'.format('brasil.gov.tiles.potd', 'test-tile'))

    def test_interface(self):
        self.assertTrue(IPersistentCoverTile.implementedBy(POTDTile))
        self.assertTrue(verifyClass(IPersistentCoverTile, POTDTile))

        tile = POTDTile(None, None)
        self.assertTrue(IPersistentCoverTile.providedBy(tile))
        self.assertTrue(verifyObject(IPersistentCoverTile, tile))

    def test_default_configuration(self):
        self.assertTrue(self.tile.is_configurable)
        self.assertTrue(self.tile.is_editable)
        self.assertTrue(self.tile.is_droppable)

    def test_accepted_content_types(self):
        self.assertListEqual(
            self.tile.accepted_ct(), ['Image'])

    def test_render_with_image(self):
        obj = self.portal['my-image']
        self.tile.populate_with_object(obj)
        rendered = self.tile()
        self.assertIn('<img ', rendered)
        self.assertIn('alt="This image was created for testing purposes"', rendered)
        self.assertTrue(self.tile.has_image)

    def test_title(self):
        obj = self.portal['my-image']
        self.tile.populate_with_object(obj)
        self.assertEqual(self.tile.data['title'], 'Test image')

    def test_description(self):
        obj = self.portal['my-image']
        self.tile.populate_with_object(obj)
        self.assertEqual(self.tile.data['description'], 'This image was created for testing purposes')

    def test_credits(self):
        obj = self.portal['my-image']
        obj.setRights('Test credits')
        self.tile.populate_with_object(obj)
        self.assertEqual(self.tile.data['photo_credits'], 'Test credits')
