# -*- coding: utf-8 -*-
from brasil.gov.tiles.testing import INTEGRATION_TESTING
from brasil.gov.tiles.tiles.destaque import DestaqueTile
from brasil.gov.tiles.tiles.destaque import IDestaqueTile
from collective.cover.controlpanel import ICoverSettings
from collective.cover.tests.base import TestTileMixin
from plone import api
from plone.registry.interfaces import IRegistry
from zope.component import getMultiAdapter
from zope.component import getUtility

import unittest


class DestaqueTileTestCase(TestTileMixin, unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        super(DestaqueTileTestCase, self).setUp()
        self.tile = DestaqueTile(self.cover, self.request)
        self.tile.__name__ = u'destaque'
        self.tile.id = u'test'

    @unittest.expectedFailure  # FIXME: raises BrokenImplementation
    def test_interface(self):
        self.interface = IDestaqueTile
        self.klass = DestaqueTile
        super(DestaqueTileTestCase, self).test_interface()

    def test_default_configuration(self):
        self.assertTrue(self.tile.is_configurable)
        self.assertTrue(self.tile.is_droppable)
        self.assertFalse(self.tile.is_editable)

    def test_tile_is_empty(self):
        self.assertTrue(self.tile.is_empty())

    def test_crud(self):
        # we start with an empty tile
        self.assertTrue(self.tile.is_empty())

        # now we add a couple of objects to the destaque
        obj1 = self.portal['my-document']
        obj2 = self.portal['my-image']
        self.tile.populate_with_object(obj1)
        self.tile.populate_with_object(obj2)

        # tile's data attributed is cached so we should re-instantiate the tile
        tile = getMultiAdapter(
            (self.cover, self.request),
            name=self.tile.__name__,
        )
        tile = tile['test']
        self.assertEqual(len(tile.results()), 2)
        self.assertTrue(obj1 in tile.results())
        self.assertTrue(obj2 in tile.results())

        # next, we replace the destaque of objects with a different one
        obj3 = self.portal['my-news-item']
        tile.replace_with_uuids([api.content.get_uuid(obj3)])
        # tile's data attributed is cached so we should re-instantiate the tile
        tile = getMultiAdapter(
            (self.cover, self.request),
            name=self.tile.__name__,
        )
        tile = tile['test']
        self.assertTrue(obj1 not in tile.results())
        self.assertTrue(obj2 not in tile.results())
        self.assertTrue(obj3 in tile.results())

        # finally, we remove it from the destaque; the tile must be empty again
        tile.remove_item(obj3.UID())
        # tile's data attributed is cached so we should re-instantiate the tile
        tile = getMultiAdapter(
            (self.cover, self.request),
            name=self.tile.__name__,
        )
        tile = tile['test']
        self.assertTrue(tile.is_empty())

    def test_populate_with_uuids(self):
        # we start with an empty tile
        self.assertTrue(self.tile.is_empty())

        # now we add a couple of objects to the destaque
        obj1 = self.portal['my-document']
        obj2 = self.portal['my-image']
        self.tile.populate_with_uuids([api.content.get_uuid(obj1),
                                      api.content.get_uuid(obj2)])

        # tile's data attributed is cached so we should re-instantiate the tile
        tile = getMultiAdapter(
            (self.cover, self.request),
            name=self.tile.__name__,
        )
        tile = tile['test']
        self.assertEqual(len(tile.results()), 2)
        self.assertTrue(obj1 in tile.results())
        self.assertTrue(obj2 in tile.results())

    def test_accepted_content_types(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ICoverSettings)  # noqa
        self.assertEqual(
            self.tile.accepted_ct(),
            settings.searchable_content_types,
        )

    def test_render_empty(self):
        msg = 'Please add up to 2 objects to the tile.'
        self.assertTrue(msg in self.tile())
