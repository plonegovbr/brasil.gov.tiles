# -*- coding: utf-8 -*-
from brasil.gov.tiles.testing import INTEGRATION_TESTING
from brasil.gov.tiles.tiles.albuns import AlbunsTile
from collective.cover.tiles.base import IPersistentCoverTile
from mock import Mock
from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from zope.component import getMultiAdapter
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject

import unittest


class AlbunsTileTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.request = self.layer['request']
        self.name = u'albuns'
        self.cover = self.portal['frontpage']
        self.tile = getMultiAdapter((self.cover, self.request), name=self.name)
        self.tile = self.tile['test']
        wf = self.portal.portal_workflow
        wf.setDefaultChain('simple_publication_workflow')

    def test_interface(self):
        self.assertTrue(IPersistentCoverTile.implementedBy(AlbunsTile))
        self.assertTrue(verifyClass(IPersistentCoverTile, AlbunsTile))

        tile = AlbunsTile(None, None)
        self.assertTrue(IPersistentCoverTile.providedBy(tile))
        self.assertTrue(verifyObject(IPersistentCoverTile, tile))

    def test_default_configuration(self):
        self.assertTrue(self.tile.is_configurable)
        self.assertTrue(self.tile.is_droppable)
        self.assertTrue(self.tile.is_editable)

    def test_accepted_content_types(self):
        self.assertEqual(self.tile.accepted_ct(), ['Folder'])

    def test_folder_tile_render(self):
        obj = self.portal['my-folder']
        obj.setLayout('galeria_de_albuns')
        self.tile.populate_with_object(obj)

        rendered = self.tile()
        msg = u'Drag an album to the popular tile.'
        self.assertIn(msg, rendered)

    def test_delete_folder(self):
        obj = self.portal['my-folder']
        obj.setLayout('galeria_de_albuns')
        self.tile.populate_with_object(obj)

        rendered = self.tile()
        msg = u'Drag an album to the popular tile.'
        self.assertIn(msg, rendered)

        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Editor', 'Reviewer'])
        login(self.portal, TEST_USER_NAME)
        self.portal.manage_delObjects(['my-folder'])

        rendered = self.tile()
        self.tile.is_compose_mode = Mock(return_value=True)
        self.assertIn(msg, rendered)

        self.tile.is_compose_mode = Mock(return_value=False)
        self.assertIn(msg, self.tile())

    def test_get_albuns(self):
        # as a File does not have an image field, we should have no scale
        gal_albuns = self.portal['my-folder']
        gal_albuns.setLayout('galeria_de_albuns')
        self.tile.populate_with_object(gal_albuns)
        self.assertEqual(self.tile.get_albuns(), [])

        gal_albuns.invokeFactory('Folder', 'galeria-de-fotos')
        gal_fotos = gal_albuns['galeria-de-fotos']
        with api.env.adopt_roles(['Manager']):
            api.content.transition(obj=gal_fotos, transition='publish')
        gal_fotos.setLayout('galeria_de_fotos')
        api.content.copy(source=self.portal['my-image'], target=gal_fotos)
        self.tile.populate_with_object(gal_albuns)
        self.assertEqual(self.tile.get_albuns(), [gal_fotos])

    def test_scale(self):
        # as a File does not have an image field, we should have no scale
        obj = self.portal['my-folder']
        obj.setLayout('galeria_de_fotos')
        api.content.copy(source=self.portal['my-file'], target=obj)
        self.assertFalse(self.tile.scale(obj))
        api.content.delete(obj=obj['my-file'])

        # as an Image does have an image field, we should have a scale
        api.content.copy(source=self.portal['my-image'], target=obj)
        scale = self.tile.scale(obj)
        self.assertTrue(scale)
        self.assertIn('src', scale)
        self.assertTrue(scale['src'])
        self.assertIn('alt', scale)
        self.assertEqual(scale['alt'], 'This image was created for testing purposes')

        # turn visibility off, we should have no thumbnail
        # XXX: refactor; we need a method to easily change field visibility
        tile_conf = self.tile.get_tile_configuration()
        tile_conf['player']['visibility'] = u'off'
        self.tile.set_tile_configuration(tile_conf)

        self.assertFalse(self.tile._field_is_visible('player'))
        self.assertTrue(self.tile.thumbnail(obj))

        # TODO: test against Dexterity-based content types

    def test_thumbnail(self):
        # as a File does not have an image field, we should have no thumbnail
        obj = self.portal['my-folder']
        obj.setLayout('galeria_de_fotos')
        api.content.copy(source=self.portal['my-file'], target=obj)
        self.assertFalse(self.tile.thumbnail(obj))
        api.content.delete(obj=obj['my-file'])

        # as an Image does have an image field, we should have a thumbnail
        api.content.copy(source=self.portal['my-image'], target=obj)
        thumbnail = self.tile.thumbnail(obj)
        self.assertTrue(thumbnail)
        self.assertIn('src', thumbnail)
        self.assertTrue(thumbnail['src'])
        self.assertIn('alt', thumbnail)
        self.assertEqual(thumbnail['alt'], 'This image was created for testing purposes')

        # turn visibility off, we should have no thumbnail
        # XXX: refactor; we need a method to easily change field visibility
        tile_conf = self.tile.get_tile_configuration()
        tile_conf['carrossel']['visibility'] = u'off'
        self.tile.set_tile_configuration(tile_conf)

        self.assertFalse(self.tile._field_is_visible('carrossel'))
        self.assertTrue(self.tile.thumbnail(obj))

        # TODO: test against Dexterity-based content types
