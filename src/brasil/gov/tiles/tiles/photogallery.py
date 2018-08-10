# -*- coding: utf-8 -*-
from brasil.gov.tiles import _
from collective.cover.interfaces import ITileEditForm
from collective.cover.tiles.list import IListTile
from collective.cover.tiles.list import ListTile
from collective.cover.widgets.textlinessortable import TextLinesSortableFieldWidget
from plone.autoform import directives as form
from plone.tiles.interfaces import ITileDataManager
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.interface import implementer


class IPhotoGalleryTile(IListTile):
    """A tile that shows an photo gallery."""

    tile_description = schema.Text(title=_(u'Tile Description'), required=False)
    form.omitted('tile_description')
    form.no_omit(ITileEditForm, 'tile_description')

    form.no_omit(ITileEditForm, 'uuids')
    form.widget(uuids=TextLinesSortableFieldWidget)


@implementer(IPhotoGalleryTile)
class PhotoGalleryTile(ListTile):
    """A tile that shows an photo gallery."""

    index = ViewPageTemplateFile('templates/photogallery.pt')
    short_name = _(u'msg_short_photo_gallery', default=u'Photo Gallery')
    is_configurable = True
    is_droppable = True
    is_editable = True
    limit = 5 * 3

    @staticmethod
    def accepted_ct():
        return ['Image']

    def get_description(self, item):
        """Get the description of the item, or the custom description
        if set.
        :param item: [required] The item for which we want the description
        :type item: Content object
        :returns: the item description
        :rtype: unicode
        """
        # First we get the url for the item itself
        description = item.Description()
        uuid = self.get_uuid(item)
        data_mgr = ITileDataManager(self)
        data = data_mgr.get()
        uuids = data['uuids']
        if uuid in uuids:
            if uuids[uuid].get('custom_description', u''):
                # If we had a custom description set, then get that
                description = uuids[uuid].get('custom_description')
        return description

    @staticmethod
    def get_credits(item):
        return item.Rights()
