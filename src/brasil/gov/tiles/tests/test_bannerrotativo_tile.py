# -*- coding: utf-8 -*-
from brasil.gov.tiles.testing import INTEGRATION_TESTING
from brasil.gov.tiles.tiles.banner_rotativo import BannerRotativoTile
from brasil.gov.tiles.tiles.banner_rotativo import IBannerRotativoTile
from brasil.gov.tiles.tiles.list import ListTile
from collective.cover.tests.base import TestTileMixin
from plone.app.imaging.interfaces import IImageScale
from zope.component import getMultiAdapter

import unittest


class BannerRotativoTileTestCase(TestTileMixin, unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        super(BannerRotativoTileTestCase, self).setUp()
        self.tile = BannerRotativoTile(self.cover, self.request)
        self.tile.__name__ = u'banner_rotativo'
        self.tile.id = u'test'

    @unittest.expectedFailure  # FIXME: raises BrokenImplementation
    def test_interface(self):
        self.interface = IBannerRotativoTile
        self.klass = BannerRotativoTile
        super(BannerRotativoTileTestCase, self).test_interface()

    def test_default_configuration(self):
        self.assertFalse(self.tile.is_configurable)
        self.assertTrue(self.tile.is_droppable)
        self.assertTrue(self.tile.is_editable)

    def test_tile_is_empty(self):
        self.assertTrue(self.tile.is_empty())

    def test_accepted_content_types(self):
        results = ListTile.accepted_ct(self.tile)
        results.append(u'ExternalContent')
        self.assertEqual(self.tile.accepted_ct(), results)

    def test_populate_with_object(self):
        # verifica a renderizacao com uma imagem
        obj = self.portal['my-image']
        self.tile.populate_with_object(obj)
        rendered = self.tile()
        msg = u'Test image'
        self.assertIn(msg, rendered)

    def test_show_nav(self):
        self.tile.data['layout'] = u'Banner'
        # retorna falso com um item
        obj = self.portal['my-image']
        self.tile.populate_with_object(obj)
        tile = getMultiAdapter(
            (self.cover, self.request),
            name=self.tile.__name__,
        )
        tile = tile['test']
        self.assertFalse(tile.show_nav())
        # retorna verdadeiro para mais de um item
        obj2 = self.portal['my-image1']
        self.tile.populate_with_object(obj2)
        obj3 = self.portal['my-image2']
        self.tile.populate_with_object(obj3)
        tile = getMultiAdapter(
            (self.cover, self.request),
            name=self.tile.__name__,
        )
        tile = tile['test']
        self.assertTrue(tile.show_nav())

    def test_thumbnail(self):
        # verifica o thumbnail
        obj = self.portal['my-image']
        thumbnail = self.tile.thumbnail(obj)
        self.assertTrue(thumbnail)
        # the thumbnail is an ImageScale
        self.assertTrue(IImageScale.providedBy(thumbnail))

    def text_show_description(self):
        # nao exibe descricao no layout de banner
        self.tile.data['layout'] = u'Banner'
        self.assertFalse(self.tile.show_description())
        # nao exibe descricao no layout de Texto sobreposto
        self.tile.data['layout'] = u'Texto sobreposto'
        self.assertFalse(self.tile.show_description())
        # exibe descricao no layout de Chamada de foto
        self.tile.data['layout'] = u'Chamada de foto'
        self.assertTrue(self.tile.show_description())

    def show_rights(self):
        # nao exibe creditos no layout de banner
        self.tile.data['layout'] = u'Banner'
        self.assertTrue(self.tile.show_rights())
        # nao exibe creditos no layout de Texto sobreposto
        self.tile.data['layout'] = u'Texto sobreposto'
        self.assertTrue(self.tile.show_rights())
        # exibe creditos no layout de Chamada de foto
        self.tile.data['layout'] = u'Chamada de foto'
        self.assertFalse(self.tile.show_rights())

    def test_layout(self):
        # verifica o layout padrao em banner
        self.tile.data['layout'] = u'Banner'
        layout = self.tile.layout_banner()
        self.assertEqual(layout, 1)
        # altera e verifica se layout retorna chamada de foto como 2
        self.tile.data['layout'] = u'Chamada de foto'
        layout = self.tile.layout_banner()
        self.assertEqual(layout, 2)
        # altera e verifica se layout retorna texto sobreposto como 3
        self.tile.data['layout'] = u'Texto sobreposto'
        layout = self.tile.layout_banner()
        self.assertEqual(layout, 3)

    def test_layout_banner(self):
        # verifica a renderizacao no layout Texto Banner
        self.tile.data['layout'] = u'Banner'
        rendered = self.tile()
        msg = u'chamada_sem_foto'
        self.assertIn(msg, rendered)
        self.assertEqual(
            self.tile.tile_class(),
            'chamada_sem_foto tile-content',
        )

    def test_layout_chamada_sem_foto(self):
        # verifica a renderizacao no layout Chamada de foto
        self.tile.data['layout'] = u'Chamada de foto'
        rendered = self.tile()
        msg = u'chamada_com_foto'
        self.assertIn(msg, rendered)
        self.assertEqual(
            self.tile.tile_class(),
            'chamada_com_foto tile-content',
        )

    def test_layout_texto_sobreposto(self):
        # verifica a renderizacao no layout Texto sobreposto
        self.tile.data['layout'] = u'Texto sobreposto'
        rendered = self.tile()
        msg = u'chamada_sobrescrito'
        self.assertIn(msg, rendered)
        self.assertEqual(
            self.tile.tile_class(),
            'chamada_sobrescrito tile-content',
        )
