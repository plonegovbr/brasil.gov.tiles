# -*- coding: utf-8 -*-
from brasil.gov.tiles.testing import BaseIntegrationTestCase
from brasil.gov.tiles.tiles.quote import QuoteTile
from collective.cover.tiles.base import IPersistentCoverTile
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject


class QuoteTileTestCase(BaseIntegrationTestCase):

    def setUp(self):
        super(QuoteTileTestCase, self).setUp()
        self.tile = self.portal.restrictedTraverse(
            '@@{0}/{1}'.format('brasil.gov.tiles.quote', 'test-tile'))

    def test_interface(self):
        self.assertTrue(IPersistentCoverTile.implementedBy(QuoteTile))
        self.assertTrue(verifyClass(IPersistentCoverTile, QuoteTile))

        tile = QuoteTile(None, None)
        self.assertTrue(IPersistentCoverTile.providedBy(tile))
        self.assertTrue(verifyObject(IPersistentCoverTile, tile))

    def test_default_configuration(self):
        self.assertTrue(self.tile.is_configurable)
        self.assertTrue(self.tile.is_editable)
        self.assertTrue(self.tile.is_droppable)

    def test_accepted_content_types(self):
        self.assertListEqual(
            self.tile.accepted_ct(), ['collective.nitf.content'])

    def test_render(self):
        quote = (
            u'Give me six hours to chop down a tree and '
            u'I will spend the first four sharpening the axe.'
        )
        author = u'Abraham Lincoln'
        self.tile.data['quote'] = quote
        self.tile.data['quote_rights'] = author
        nitf = self.portal['my-news-folder']['my-nitf-with-image']
        self.tile.populate_with_object(nitf)
        rendered = self.tile()
        self.assertIn(quote, rendered)
        self.assertIn(author, rendered)

    def test_color_class(self):
        self.assertEqual(self.tile.color_class(), u'quote-blue')
        self.tile.data['quote_color'] = u'green'
        self.assertEqual(self.tile.color_class(), u'quote-green')
