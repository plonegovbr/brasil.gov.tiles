# -*- coding: utf-8 -*-
from brasil.gov.tiles import _
from collective.cover.tiles.base import IPersistentCoverTile
from collective.cover.tiles.base import PersistentCoverTile
from collective.cover.tiles.configuration_view import IDefaultConfigureForm
from plone import api
from plone.app.uuid.utils import uuidToObject
from plone.autoform import directives as form
from plone.tiles.interfaces import ITileDataManager
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema


class IAlbunsTile(IPersistentCoverTile):
    """
    """

    title = schema.TextLine(
        title=_(u'Title'),
        required=False,
    )
    form.omitted('player')
    form.no_omit(IDefaultConfigureForm, 'player')
    player = schema.Text(
        title=_(u'Current image'),
        required=False,
    )
    form.omitted('carrossel')
    form.no_omit(IDefaultConfigureForm, 'carrossel')
    carrossel = schema.Text(
        title=_(u'Carousel of images'),
        required=False,
    )
    form.omitted('footer')
    form.no_omit(IDefaultConfigureForm, 'footer')
    footer = schema.Text(
        title=_(u'Footer'),
        required=False,
    )

    form.no_omit('link_text')
    form.omitted(IDefaultConfigureForm, 'link_text')
    link_text = schema.TextLine(
        title=_(u'Text footer'),
        required=False,
    )
    form.no_omit('link_url')
    form.omitted(IDefaultConfigureForm, 'link_url')
    link_url = schema.TextLine(
        title=_(u'Link footer'),
        required=False,
    )


class AlbunsTile(PersistentCoverTile):
    index = ViewPageTemplateFile('templates/albuns.pt')
    is_configurable = True
    limit = 1

    def populate_with_object(self, obj):
        super(AlbunsTile, self).populate_with_object(obj)  # check permissions

        if ((obj.portal_type in self.accepted_ct()) and
           (obj.getLayout() == 'galeria_de_albuns')):
            title = _(u'Gallery albums')
            link_url = obj.absolute_url()
            link_text = _(u'Access all Albums')
            uuid = api.content.get_uuid(obj)
            data_mgr = ITileDataManager(self)
            data_mgr.set({
                'title': title,
                'link_url': link_url,
                'link_text': link_text,
                'player': True,
                'carrossel': True,
                'footer': True,
                'uuid': uuid,
            })

    def accepted_ct(self):
        """ Return a list of content types accepted by the tile.
        """
        return ['Folder']

    def get_albuns(self):
        """ Return a list of albuns
        """
        albuns = []
        uuid = self.data.get('uuid', None)
        obj = None
        if uuid:
            obj = uuidToObject(uuid)
        if obj:
            catalog = api.portal.get_tool('portal_catalog')

            # Procuro todas subpastas na pasta do album
            path = '/'.join(obj.getPhysicalPath())
            brains = catalog(Type='Folder',
                             path={'query': path},
                             sort_on='effective',
                             sort_order='reverse',
                             review_state='published')[:10]
            # Procuro todas subpastas na pasta do album

            # Retiro as pastas que não são albuns
            for brain in brains:
                obj = brain.getObject()
                if (obj.getLayout() == 'galeria_de_fotos'):
                    albuns.append(obj)
            # Retiro as pastas que não são albuns

        return albuns

    def scale(self, item):
        catalog = api.portal.get_tool('portal_catalog')
        path = '/'.join(item.getPhysicalPath())
        brains = catalog(Type=['Image', 'Folder'],
                         path={'query': path,
                               'depth': 1},
                         sort_on='getObjPositionInParent')
        if len(brains) > 0:
            brain = brains[0]
            if brain.Type == 'Image':
                image = brain.getObject()
                scales = image.restrictedTraverse('@@images')
                thumb = scales.scale('image', 'tile_album_view')
                return {
                    'src': thumb.url,
                    'alt': image.Description(),
                }

    def thumbnail(self, item):
        catalog = api.portal.get_tool('portal_catalog')
        path = '/'.join(item.getPhysicalPath())
        brains = catalog(Type=['Image', 'Folder'],
                         path={'query': path,
                               'depth': 1},
                         sort_on='getObjPositionInParent')
        if len(brains) > 0:
            brain = brains[0]
            if brain.Type == 'Image':
                image = brain.getObject()
                scales = image.restrictedTraverse('@@images')
                thumb = scales.scale('image', 'tile_album_thumb')
                return {
                    'src': thumb.url,
                    'alt': image.Description(),
                }
