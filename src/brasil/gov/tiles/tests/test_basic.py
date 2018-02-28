# -*- coding: utf-8 -*-
from brasil.gov.tiles.testing import BaseIntegrationTestCase
from brasil.gov.tiles.tiles.basic import BasicTile
from collective.cover.controlpanel import ICoverSettings
from collective.cover.tiles.base import IPersistentCoverTile
from plone import api
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject


class BasicTileTestCase(BaseIntegrationTestCase):

    def setUp(self):
        super(BasicTileTestCase, self).setUp()
        self.tile = self.portal.restrictedTraverse(
            '{0}/{1}'.format('collective.cover.basic', 'test-tile'),
        )

    def test_interface(self):
        self.assertTrue(IPersistentCoverTile.implementedBy(BasicTile))
        self.assertTrue(verifyClass(IPersistentCoverTile, BasicTile))

        tile = BasicTile(None, None)
        self.assertTrue(IPersistentCoverTile.providedBy(tile))
        self.assertTrue(verifyObject(IPersistentCoverTile, tile))

    def test_default_configuration(self):
        self.assertTrue(self.tile.is_configurable)
        self.assertTrue(self.tile.is_droppable)
        self.assertTrue(self.tile.is_editable)

    def test_accepted_content_types(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ICoverSettings)  # noqa
        self.assertEqual(
            self.tile.accepted_ct(),
            settings.searchable_content_types,
        )

    def test_render_empty(self):
        rendered = self.tile()
        msg = u'Please drag&amp;drop some content here to populate the tile.'
        self.assertIn(msg, rendered)
        self.assertTrue(self.tile.is_empty)

    def test_render_with_image(self):
        obj = self.portal['my-image']
        self.tile.populate_with_object(obj)
        rendered = self.tile()
        self.assertIn('<img ', rendered)
        self.assertIn(
            'alt="This image was created for testing purposes"',
            rendered,
        )

    def test_render_with_link(self):
        obj = self.portal['my-link']
        self.tile.populate_with_object(obj)
        rendered = self.tile()
        self.assertNotIn('<img ', rendered)
        self.assertIn(
            '<a class="imag" href="http://nohost/plone/my-link"',
            rendered,
        )

    def test_Subject(self):
        obj = self.portal['my-image']
        self.tile.populate_with_object(obj)
        self.assertEqual(self.tile.Subject(), ())

    def test_getURL(self):
        obj = self.portal['my-image']
        self.tile.populate_with_object(obj)
        self.assertEqual(self.tile.getURL(), 'http://nohost/plone/my-image')

    def test_variacao_titulo(self):
        obj = self.portal['my-image']
        self.tile.populate_with_object(obj)
        self.assertEqual(self.tile.variacao_titulo(), None)

    def test_nova_estrutura_icon_tiles(self):
        """
        FIXME: bin/instance está diferente de bin/test. Nesse contexto,
        o método que retorna a tile e suas características, por algum motivo
        retorna "None" no atributo 'icon' quando executamos bin/test: nesse
        contexto, a template, ao receber None, popula o html com
        tile-generic.png.

        Com a nova versão de collective.cover, > 1.0a12, ele já retorna /img/tile
        na template ao invés de só /tile e esse teste verifica isso, mas
        renderizando o html da view.

        Quando o issue

            https://github.com/plone/plone.app.testing/issues/27

        for finalizado, ele pode auxiliar na forma de melhorar esse teste, por
        exemplo, apenas chamando o método "get_tile_metadata" de @@tile_list ao
        invés de renderizar o html.

        """
        with api.env.adopt_roles(roles=['Manager']):
            api.content.create(
                type='collective.cover.content',
                title='my-cover',
                id='my-cover',
                container=self.portal,
                template_layout='Layout A',
            )
            # A partir da versão 1.3b1 de collective.cover, com a remoção do
            # grok, essa view que tinha a permissão de 'zope2.View' passa a ter
            # 'collective.cover.CanEditLayout'.
            view = self.portal['my-cover'].restrictedTraverse('@@tile_list')
        html = view()
        prefix_icon = '<img src="++resource++collective'
        total_in_rendered_view = html.count(prefix_icon)
        self.assertTrue(len(view.tiles) == total_in_rendered_view)
