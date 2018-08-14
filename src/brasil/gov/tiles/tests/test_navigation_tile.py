# -*- coding: utf-8 -*-
from brasil.gov.tiles.testing import BaseIntegrationTestCase
from brasil.gov.tiles.tiles.navigation import NavigationTile
from collective.cover.tiles.base import IPersistentCoverTile
from plone import api
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject


class NavigationTileTestCase(BaseIntegrationTestCase):

    def setUp(self):
        super(NavigationTileTestCase, self).setUp()
        self.tile = self.portal.restrictedTraverse(
            '@@{0}/{1}'.format('brasil.gov.tiles.navigation', 'test-tile'))
        self.portal.portal_workflow.setDefaultChain('simple_publication_workflow')

    def test_interface(self):
        self.assertTrue(IPersistentCoverTile.implementedBy(NavigationTile))
        self.assertTrue(verifyClass(IPersistentCoverTile, NavigationTile))

        tile = NavigationTile(None, None)
        self.assertTrue(IPersistentCoverTile.providedBy(tile))
        self.assertTrue(verifyObject(IPersistentCoverTile, tile))

    def test_default_configuration(self):
        self.assertFalse(self.tile.is_configurable)
        self.assertFalse(self.tile.is_editable)
        self.assertFalse(self.tile.is_droppable)

    def test_render_in_root(self):

        with api.env.adopt_roles(['Manager']):

            cover = api.content.create(
                self.portal, 'collective.cover.content', 'cover1')

            obj1 = self.portal['my-folder']
            obj2 = self.portal['my-news-folder']
            obj3 = self.portal['mandelbrot-set']
            obj4 = self.portal['my-news-item']

            api.content.transition(obj=obj1, transition='publish')
            api.content.transition(obj=obj2, transition='publish')
            api.content.transition(obj=obj3, transition='publish')
            api.content.transition(obj=obj4, transition='publish')

        rendered = cover.restrictedTraverse(
            '@@{0}/{1}'.format('brasil.gov.tiles.navigation', 'test-tile'))()

        self.assertIn('<h2 class="navigation-title">Plone site</h2>', rendered)
        self.assertIn('<a href="http://nohost/plone/my-news-item">Test news item</a>', rendered)
        self.assertIn('<li class="navigation-more"><a href="#">Mais</a></li>', rendered)

    def test_render_in_folder(self):

        with api.env.adopt_roles(['Manager']):

            cover = api.content.create(
                self.portal['my-news-folder'], 'collective.cover.content', 'cover1')

            obj1 = self.portal['my-news-folder']['my-nitf-without-image']
            obj2 = self.portal['my-news-folder']['my-nitf-with-image']

            api.content.transition(obj=obj1, transition='publish')
            api.content.transition(obj=obj2, transition='publish')

        rendered = cover.restrictedTraverse(
            '@@{0}/{1}'.format('brasil.gov.tiles.navigation', 'test-tile'))()

        self.assertIn('<h2 class="navigation-title">my-news-folder</h2>', rendered)
        self.assertIn('<a href="http://nohost/plone/my-news-folder/my-nitf-with-image">my-nitf-with-image</a>', rendered)

    def test_render_with_exclude_from_nav(self):

        with api.env.adopt_roles(['Manager']):

            cover = api.content.create(
                self.portal['my-news-folder'], 'collective.cover.content', 'cover1')

            obj1 = self.portal['my-news-folder']['my-nitf-without-image']
            obj2 = self.portal['my-news-folder']['my-nitf-with-image']
            obj2.exclude_from_nav = True

            api.content.transition(obj=obj1, transition='publish')
            api.content.transition(obj=obj2, transition='publish')

        rendered = cover.restrictedTraverse(
            '@@{0}/{1}'.format('brasil.gov.tiles.navigation', 'test-tile'))()

        self.assertIn('<h2 class="navigation-title">my-news-folder</h2>', rendered)
        self.assertNotIn('<a href="http://nohost/plone/my-news-folder/my-nitf-with-image">my-nitf-with-image</a>', rendered)
        self.assertIn('<a href="http://nohost/plone/my-news-folder/my-nitf-without-image">my-nitf-without-image</a>', rendered)
