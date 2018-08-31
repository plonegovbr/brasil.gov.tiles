# -*- coding: utf-8 -*-
from six.moves import range  # noqa: I001
from brasil.gov.tiles import _
from brasil.gov.tiles.tiles.list import IListTile
from brasil.gov.tiles.tiles.list import ListTile
from plone import api
from plone.tiles.interfaces import ITileDataManager
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.interface import implementer


class IAudioGalleryTile(IListTile):
    """A droppable tile that shows a gallery of audios with
    descriptions and links.
    """

    header = schema.TextLine(
        title=_(u'Header'),
        required=False,
    )

    title = schema.TextLine(
        title=_(u'Title'),
        required=False,
    )

    footer_text = schema.TextLine(
        title=_(u'Footer Link'),
        required=False,
        readonly=False,
    )

    uuids = schema.List(
        title=_(u'Audios'),
        value_type=schema.TextLine(),
        required=False,
        readonly=True,
    )


@implementer(IAudioGalleryTile)
class AudioGalleryTile(ListTile):
    """A droppable tile that shows a gallery of audios with
    descriptions and links.
    """

    index = ViewPageTemplateFile('templates/audiogallery.pt')
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

    @staticmethod
    def accepted_ct():
        """Return a list of content types accepted by the tile."""
        return ['Collection', 'Folder']

    @staticmethod
    def get_uuid(obj):
        return api.content.get_uuid(obj)

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
                catalog_results = obj.getFolderContents({'portal_type': 'File'})
                limit = len(catalog_results) if catalog_results else 0

            if catalog_results:
                limit = limit if limit <= self.limit else self.limit
                for i in range(limit):
                    results.append(catalog_results[i].getObject())

        return results

    @staticmethod
    def get_item_url(item):
        """
        Return the audio file url
        Arguments:
        - `item`: audio item
        """
        url = ''

        if (item.portal_type == 'Audio'):
            url = ';'.join([a.absolute_url() for a in item.listFolderContents()])
        else:
            url = item.absolute_url()
        return url

    def show_header(self):
        return self._field_is_visible('header')

    def init_js(self):
        return """
$(document).ready(function() {{
    $('#audiogallery-{0}').audiogallery();
}});
""".format(self.id)
