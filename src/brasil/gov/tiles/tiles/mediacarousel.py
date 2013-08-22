# -*- coding: utf-8 -*-

from collective.cover import _
from collective.cover.tiles.list import IListTile
from collective.cover.tiles.list import ListTile
from plone.autoform import directives as form
from collective.cover.tiles.configuration_view import IDefaultConfigureForm
from plone.tiles.interfaces import ITileDataManager
from plone.uuid.interfaces import IUUID
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

    footer_text = schema.TextLine(
        title=_(u'Footer Link'),
        required=False,
        readonly=False,
    )

    form.omitted('uuids')
    form.no_omit(IDefaultConfigureForm, 'uuids')
    uuids = schema.List(
        title=_(u'Elements'),
        value_type=schema.TextLine(),
        required=False,
    )


class MediaCarouselTile(ListTile):
    index = ViewPageTemplateFile("templates/mediacarousel.pt")
    is_configurable = True
    is_editable = True

    def populate_with_object(self, obj):
        super(ListTile, self).populate_with_object(obj)  # check permission

        #here we should check if the embeded item has its a video
        # XXX

        self.set_limit()
        header = obj.Title()  # use collection's title as header
        uuid = IUUID(obj, None)
        data_mgr = ITileDataManager(self)

        old_data = data_mgr.get()
        old_data['header'] = header
        old_data['uuids'] = [uuid]
        data_mgr.set(old_data)

    def get_uid(self, obj):
        return IUUID(obj)

    def thumbnail(self, item):
        scales = item.restrictedTraverse('@@images')
        try:
            return scales.scale('image', width=80, height=60)
        except:
            return None

    def scale(self, item):
        scales = item.restrictedTraverse('@@images')
        try:
            return scales.scale('image', width=692, height=433)
        except:
            return None

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
                    "portal_type": ['sc.embedder',
                                    'Image',
                                    'collective.nitf.content']
                })
                limit = len(catalog_results) if catalog_results else 0

            if catalog_results:
                limit = limit if limit <= self.limit else self.limit
                for i in xrange(limit):
                    results.append(catalog_results[i].getObject())

        return results

    def get_media_url(self, obj):
        portal_type = obj.getPortalTypeName()
        url = ''
        if portal_type == "sc.embedder":
            url = obj.url
        elif portal_type == 'Image':
            url = obj.absolute_url() + '/@@images/image'
        elif portal_type == 'collective.nitf.content':
            scale = self.scale(obj)
            url = scale.url

        return url

    def get_rights(self, obj):
        rights = obj.Rights() if hasattr(obj, 'Rights') else None
        return rights

    def show_header(self):
        return self._field_is_visible('header')

    def init_js(self):
        return """
$(document).ready(function() {
    $('#mediacarousel-gallerie-%s').mediacarousel();
});
""" % (self.id)
