# -*- coding: utf-8 -*-
from future.builtins import range  # isort:skip
from brasil.gov.tiles import _ as _
from brasil.gov.tiles.tiles.list import IListTile
from brasil.gov.tiles.tiles.list import ListTile
from collective.cover.tiles.configuration_view import IDefaultConfigureForm
from plone import api
from plone.autoform import directives as form
from plone.namedfile.field import NamedBlobImage as NamedImage
from plone.tiles.interfaces import ITileDataManager
from Products.CMFPlone.utils import safe_hasattr
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema


class IMediaCarouselTile(IListTile):
    """
    """

    header = schema.TextLine(
        title=_(u'Header'),
        required=False,
    )

    form.omitted('title')
    form.no_omit(IDefaultConfigureForm, 'title')
    title = schema.TextLine(
        title=_(u'Title'),
        required=False,
    )

    form.omitted('image')
    form.no_omit(IDefaultConfigureForm, 'image')
    image = NamedImage(
        title=_(u'Image'),
        required=False,
        readonly=True,
    )

    form.omitted('uuids')
    form.no_omit(IDefaultConfigureForm, 'uuids')
    uuids = schema.List(
        title=_(u'Elements'),
        value_type=schema.TextLine(),
        required=False,
    )

    footer_text = schema.TextLine(
        title=_(u'Footer Link'),
        required=False,
        readonly=False,
    )


class MediaCarouselTile(ListTile):
    index = ViewPageTemplateFile('templates/mediacarousel.pt')
    is_configurable = True
    is_editable = True

    def populate_with_object(self, obj):
        super(ListTile, self).populate_with_object(obj)  # check permission

        # here we should check if the embeded item has its a video
        # XXX

        self.set_limit()
        header = obj.Title()  # use collection's title as header
        uuid = api.content.get_uuid(obj)
        data_mgr = ITileDataManager(self)

        old_data = data_mgr.get()
        old_data['header'] = header
        old_data['uuids'] = [uuid]
        data_mgr.set(old_data)

    def get_uuid(self, obj):
        return api.content.get_uuid(obj)

    def thumbnail(self, item):
        if self._has_image_field(item):
            scales = item.restrictedTraverse('@@images')
            return scales.scale('image', width=80, height=60)

    def scale(self, item):
        if self._has_image_field(item):
            scales = item.restrictedTraverse('@@images')
            return scales.scale('image', width=692, height=433)

    def accepted_ct(self):
        """ Return a list of content types accepted by the tile.
        """
        return ['Collection', 'Folder']

    def get_elements(self, obj):
        results = []
        if obj:
            portal_type = obj.getPortalTypeName()

            limit = 0
            catalog_results = []
            if portal_type == 'Collection':
                catalog_results = obj.results()
                limit = catalog_results.length if catalog_results else 0
            elif portal_type == 'Folder':
                catalog_results = obj.getFolderContents({
                    'portal_type': ['sc.embedder',
                                    'Image',
                                    'collective.nitf.content'],
                })
                limit = len(catalog_results) if catalog_results else 0

            if catalog_results:
                limit = limit if limit <= self.limit else self.limit
                for i in range(limit):
                    results.append(catalog_results[i].getObject())

        return results

    def get_media_url(self, obj):
        portal_type = obj.getPortalTypeName()
        url = ''
        if portal_type == 'sc.embedder':
            url = obj.url
        elif portal_type == 'Image':
            url = obj.absolute_url() + '/@@images/image'
        elif portal_type == 'collective.nitf.content':
            scale = self.scale(obj)
            if scale is not None:
                url = scale.url
            else:
                url = obj.absolute_url()

        return url

    def get_rights(self, obj):
        rights = obj.Rights() if safe_hasattr(obj, 'Rights') else None
        return rights

    def show_header(self):
        return self._field_is_visible('header')

    def get_title(self, item):
        title = ''
        if self._field_is_visible('title'):
            title = '<a href="' + item.absolute_url() + '/view">' + item.title + '</a>'
        return title

    def get_description(self, item):
        description = ''
        if self._field_is_visible('description'):
            description = item.Description()
        return description

    def init_js(self):
        return """
$(document).ready(function() {{
    $('#mediacarousel-gallerie-{0}').mediacarousel();
}});
""".format(self.id)
