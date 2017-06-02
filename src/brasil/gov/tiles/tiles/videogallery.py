# -*- coding: utf-8 -*-
from brasil.gov.tiles import _ as _
from collective.cover.tiles.configuration_view import IDefaultConfigureForm
from collective.cover.tiles.list import IListTile
from collective.cover.tiles.list import ListTile
from plone.directives import form
from plone.namedfile.field import NamedBlobImage as NamedImage
from plone.tiles.interfaces import ITileDataManager
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.interface import implementer


class IVideoGalleryTile(IListTile, form.Schema):
    """
    """

    subtitle = schema.TextLine(
        title=_(u'Subtitle'),
        required=False,
        readonly=False,
    )

    # FIXME: Ver a documentação em mediacarousel.py.
    footer_text = schema.TextLine(
        title=_(u'Footer Link'),
        required=False,
        readonly=False,
    )

    # FIXME: Ver como migrar NamedImage para NamedBlobImage, como está previsto
    # em https://github.com/collective/collective.cover/blob/1.1b1/src/collective/cover/tiles/list.py#L66
    form.omitted('image')
    form.no_omit(IDefaultConfigureForm, 'image')
    image = NamedImage(
        title=_(u'Image'),
        required=False,
        readonly=True,
    )


@implementer(IVideoGalleryTile)
class VideoGalleryTile(ListTile):

    index = ViewPageTemplateFile('templates/videogallery.pt')
    limit = 6
    short_name = _(u'Video Gallery', default=u'Video Gallery')

    def populate_with_object(self, obj):
        super(VideoGalleryTile, self).populate_with_object(obj)
        # XXX: Ver a documentação em mediacarousel.py.
        data_mgr = ITileDataManager(self)
        old_data = data_mgr.get()
        old_data['tile_title'] = obj.Title()
        old_data['footer_text'] = obj.absolute_url()
        # Uso na template para compor o id do item de video na tag <a>.
        old_data['uuid_container'] = self.get_uuid(obj)
        data_mgr.set(old_data)

    def accepted_ct(self):
        """ Return a list of content types accepted by the tile.
        """
        return ['Collection', 'Folder']

    def thumbnail(self, item):
        if self._has_image_field(item):
            scales = item.restrictedTraverse('@@images')
            return scales.scale('image', width=80, height=60)

    def show_tile_title(self):
        # FIXME: Ver documentação no mesmo método em mediacarousel.py.
        return self._field_is_visible('tile_title')

    def results(self):
        valid_portal_types = ['sc.embedder']
        return super(VideoGalleryTile, self).results(portal_type=valid_portal_types)
