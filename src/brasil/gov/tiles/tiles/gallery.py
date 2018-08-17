# -*- coding: utf-8 -*-
from brasil.gov.tiles import _
from brasil.gov.tiles.widgets.textlines_sortable_subtitle import TextLinesSortableSubtitleFieldWidget
from collective.cover.interfaces import ITileEditForm
from collective.cover.tiles.carousel import CarouselTile
from collective.cover.tiles.list import IListTile
from plone.autoform import directives as form
from plone.dexterity.interfaces import IDexterityContent
from plone.tiles.interfaces import ITileDataManager
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.interface import implementer


class IGalleryTile(IListTile):
    """Display a gallery of items."""

    tile_description = schema.Text(title=_(u'Tile Description'), required=False)
    form.omitted('tile_description')
    form.no_omit(ITileEditForm, 'tile_description')

    form.no_omit(ITileEditForm, 'uuids')
    form.widget(uuids=TextLinesSortableSubtitleFieldWidget)


@implementer(IGalleryTile)
class GalleryTile(CarouselTile):
    """Display a gallery of items."""

    index = ViewPageTemplateFile('templates/gallery.pt')
    short_name = _(u'msg_short_name_gallery', default=u'Gallery')

    is_configurable = False
    is_droppable = True
    is_editable = True
    limit = 5 * 3

    @property
    def tile_description(self):
        return self.data['tile_description']

    @staticmethod
    def autoplay():
        """Method for override acquired in inheritance."""
        return True

    def get_subtitle(self, item):
        """Get the subtitle of the item, or the custom subtitle if set.

        :param item: [required] The item for which we want the subtitle
        :type item: Content object
        :returns: the item subtitle
        :rtype: unicode
        """
        # First we get the subtitle for the item itself
        subtitle = getattr(item, 'subtitle', None)
        uuid = self.get_uuid(item)
        data_mgr = ITileDataManager(self)
        data = data_mgr.get()
        uuids = data['uuids']
        if uuid in uuids:
            if uuids[uuid].get('custom_subtitle', u''):
                # If we had a custom subtitle set, then get that
                subtitle = uuids[uuid].get('custom_subtitle')
        return subtitle

    @staticmethod
    def thumbnail(item, scale=None):
        """Return the thumbnail of an image if the item has an image field and
        the field is visible in the tile.
        :param item: [required]
        :param scale: scale
        :type item: content object
        """
        if scale is None and not IDexterityContent.providedBy(item):
            scale = 'large'
        scales = item.restrictedTraverse('@@images')
        return scales.scale('image', scale)
