# -*- coding: utf-8 -*-

from collective.cover import _
from collective.cover.tiles.base import IPersistentCoverTile
from collective.cover.tiles.base import PersistentCoverTile
from plone.tiles.interfaces import ITileDataManager
from plone.uuid.interfaces import IUUID
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema


class IAudioTile(IPersistentCoverTile):
    """
    """

    title = schema.TextLine(
        title=_(u'Title'),
        required=False,
    )

    description = schema.TextLine(
        title=_(u'Description'),
        required=False,
        readonly=False,
    )

    credit = schema.TextLine(
        title=_(u'Credit'),
        required=False,
        readonly=False,
    )

    uuids = schema.List(
        title=_(u'Audio'),
        value_type=schema.TextLine(),
        required=False,
        readonly=True,
    )


class AudioTile(PersistentCoverTile):
    index = ViewPageTemplateFile("templates/audio.pt")
    is_configurable = False
    is_editable = True
    limit = 1

    def populate_with_object(self, obj):
        super(AudioTile, self).populate_with_object(obj)  # check permissions

        if obj.portal_type in self.accepted_ct():
            title = obj.Title()
            description = obj.Description()
            rights = obj.Rights()
            mp3 = obj.return_mp3()
            if mp3:
                url = mp3.absolute_url()
                content_type = 'audio/mp3'
            else:
                url = obj.absolute_url()
                content_type = ''
            uuid = IUUID(obj)
            data_mgr = ITileDataManager(self)
            data_mgr.set({'title': title,
                          'description': description,
                          'url': url,
                          'credit': rights,
                          'uuid': uuid,
                          'content_type': content_type
                          })

    def accepted_ct(self):
        """ Return a list of content types accepted by the tile.
        """
        return ['Audio']

    def get_uid(self, obj):
        return IUUID(obj)

    def init_js(self):
        return """
$(document).ready(function() {
    $('#audio_jplayer_%s').audio_player({'cssSelectorAncestor':'#audio_jpcontainer_%s'});
});
""" % (self.id, self.id)
