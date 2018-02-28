# -*- coding: utf-8 -*-

from brasil.gov.tiles.testing import generate_jpeg
from brasil.gov.tiles.testing import INTEGRATION_TESTING
from brasil.gov.tiles.tiles.collection import CollectionTile
from brasil.gov.tiles.tiles.collection import ICollectionTile
from collective.cover.tests.base import TestTileMixin
from plone import api

import unittest


FLAG = 'get_alt_test'
PORTAL_SUFIX = 'plone'
NITF_FOLDER = 'collection-tile'
COLLECTION_QUERY = [
    dict(
        i='portal_type',
        o='plone.app.querystring.operation.selection.is',
        v='collective.nitf.content',
    ),
    dict(
        i='path',
        o='plone.app.querystring.operation.string.path',
        v='/{0}/{1}'.format(PORTAL_SUFIX, NITF_FOLDER),
    ),
    dict(
        i='Subject',
        o='plone.app.querystring.operation.selection.is',
        v=FLAG,
    ),
]


class CollectionTileTestCase(TestTileMixin, unittest.TestCase):

    layer = INTEGRATION_TESTING

    def _tile(self):
        self.tile = CollectionTile(self.cover, self.request)
        self.tile.__name__ = u'collective.cover.collection'
        self.tile.id = u'test'

    def setUp(self):
        super(CollectionTileTestCase, self).setUp()
        self._tile()

    @unittest.expectedFailure  # FIXME: raises BrokenImplementation
    def test_interface(self):
        self.interface = ICollectionTile
        self.klass = CollectionTile
        super(CollectionTileTestCase, self).test_interface()

    def test_default_configuration(self):
        self.assertTrue(self.tile.is_configurable)
        self.assertTrue(self.tile.is_editable)
        self.assertTrue(self.tile.is_droppable)

    def test_accepted_content_types(self):
        self.assertEqual(self.tile.accepted_ct(), ['Collection'])

    def _create_nitf_objs(self):
        with api.env.adopt_roles(['Manager']):
            api.content.create(
                type='Folder',
                title=NITF_FOLDER,
                container=self.portal,
            )

            # description-image: imagem tem descrição e é ela que tem de aparecer
            # no atributo alt.
            api.content.create(
                type='collective.nitf.content',
                title='description-image',
                container=self.portal[NITF_FOLDER],
            )
            api.content.create(
                type='Image',
                title='description-image-title',
                description='description-image-description',
                container=self.portal[NITF_FOLDER]['description-image'],
            ).setImage(generate_jpeg(50, 50))

            # title-image: imagem sem descrição mas com title, e é ele que tem de
            # de aparecer no atributo alt.
            api.content.create(
                type='collective.nitf.content',
                title='title-image',
                container=self.portal[NITF_FOLDER],
            )
            api.content.create(
                type='Image',
                title='title-image-title',
                container=self.portal[NITF_FOLDER]['title-image'],
            ).setImage(generate_jpeg(50, 50))

            # description-nitf: imagem sem título e descrição, mas notícia com
            # descrição, e é ela que tem de aparecer no atributo alt.
            api.content.create(
                type='collective.nitf.content',
                title='description-nitf',
                description='description-nitf-description',
                container=self.portal[NITF_FOLDER],
            )
            api.content.create(
                type='Image',
                id='description-nitf',
                container=self.portal[NITF_FOLDER]['description-nitf'],
            ).setImage(generate_jpeg(50, 50))

            # title-nitf: imagem sem título e descrição e notícia sem descrição,
            # é o título da notícia que tem de aparecer no atributo alt.
            api.content.create(
                type='collective.nitf.content',
                title='title-nitf',
                container=self.portal[NITF_FOLDER],
            )
            api.content.create(
                type='Image',
                id='title-nitf',
                container=self.portal[NITF_FOLDER]['title-nitf'],
            ).setImage(generate_jpeg(50, 50))

            self.portal[NITF_FOLDER].reindexObject()

    def _create_nitf_collection(self):
        with api.env.adopt_roles(['Manager']):
            obj = api.content.create(
                self.portal,
                'Collection',
                'collection-get-alt',
                query=COLLECTION_QUERY,
            )
            api.content.transition(obj, 'publish')
            assert len(obj.results()) == 1
        return obj

    def _get_rendered_tile(self, tile_title):
        self.portal[NITF_FOLDER][tile_title].setSubject(FLAG)
        self.portal[NITF_FOLDER][tile_title].reindexObject(idxs=['subject'])
        obj = self._create_nitf_collection()
        self.tile.populate_with_object(obj)
        rendered = self.tile()
        self.portal[NITF_FOLDER][tile_title].setSubject('')
        self.portal[NITF_FOLDER][tile_title].reindexObject(idxs=['subject'])
        api.content.delete(obj)
        return rendered

    def test_get_alt(self):
        self._create_nitf_objs()

        # Criaremos uma coleção de apenas uma notícia para testar a situação
        # proposta em get_alt: dessa forma, facilita o teste que verifica se
        # a renderização possui uma string específica ou não. A forma de fazer
        # isso é setando uma tag, que será usada como flag.

        rendered = self._get_rendered_tile('description-image')
        self.assertIn('alt="description-image-description"', rendered)

        self._tile()
        rendered = self._get_rendered_tile('title-image')
        self.assertIn('alt="title-image-title"', rendered)

        self._tile()
        rendered = self._get_rendered_tile('description-nitf')
        self.assertIn('alt="description-nitf-description"', rendered)

        self._tile()
        rendered = self._get_rendered_tile('title-nitf')
        self.assertIn('alt="title-nitf"', rendered)
