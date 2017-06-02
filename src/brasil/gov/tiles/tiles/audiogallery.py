# -*- coding: utf-8 -*-
from brasil.gov.tiles import _ as _
from collective.cover.tiles.list import IListTile
from collective.cover.tiles.list import ListTile
from plone.tiles.interfaces import ITileDataManager
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.interface import implementer

import pkg_resources


class IAudioGalleryTile(IListTile):
    """
    """

    # FIXME: Ver a documentação em mediacarousel.py.
    footer_text = schema.TextLine(
        title=_(u'Footer Link'),
        required=False,
        readonly=False,
    )


@implementer(IAudioGalleryTile)
class AudioGalleryTile(ListTile):
    index = ViewPageTemplateFile('templates/audiogallery.pt')
    short_name = _(u'Audio Gallery', default=u'Audio Gallery')

    def populate_with_object(self, obj):
        super(AudioGalleryTile, self).populate_with_object(obj)
        # XXX: Ver a documentação em mediacarousel.py.
        data_mgr = ITileDataManager(self)
        old_data = data_mgr.get()
        old_data['tile_title'] = obj.Title()
        old_data['footer_text'] = obj.absolute_url()
        data_mgr.set(old_data)

    def accepted_ct(self):
        """ Return a list of content types accepted by the tile.
        """
        return ['Collection', 'Folder']

    def get_item_url(self, item):
        """
        Return the audio file url
        Arguments:
        - `item`: audio item
        """
        url = ''

        if (item.portal_type == 'Audio'):
            url = ';'.join(
                [a.absolute_url() for a in item.listFolderContents()]
            )
        else:
            url = item.absolute_url()
        return url

    def show_tile_title(self):
        # FIXME: Ver documentação no mesmo método em mediacarousel.py.
        return self._field_is_visible('tile_title')

    def results(self):
        valid_portal_types = ['File']
        try:
            pkg_resources.get_distribution('brasil.gov.portal')
            valid_portal_types.append('Audio')
            valid_portal_types.append('MPEG Audio File')
            valid_portal_types.append('OGG Audio File')
        except pkg_resources.DistributionNotFound:
            pass
        return super(AudioGalleryTile, self).results(portal_type=valid_portal_types)

    def init_js(self):
        return """
$(document).ready(function() {
    $('#audiogallery-%s').audiogallery();
});
""" % (self.id)
