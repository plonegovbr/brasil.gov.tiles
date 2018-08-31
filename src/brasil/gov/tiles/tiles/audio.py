# -*- coding: utf-8 -*-
from brasil.gov.tiles import _
from collective.cover.tiles.base import IPersistentCoverTile
from collective.cover.tiles.base import PersistentCoverTile
from plone import api
from plone.tiles.interfaces import ITileDataManager
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.interface import implementer


class IAudioTile(IPersistentCoverTile):
    """A droppable tile that shows an audio player with description,
    link and credits.
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


@implementer(IAudioTile)
class AudioTile(PersistentCoverTile):
    """A droppable tile that shows an audio player with description,
    link and credits.
    """

    index = ViewPageTemplateFile('templates/audio.pt')
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
            uuid = api.content.get_uuid(obj)
            data_mgr = ITileDataManager(self)
            data_mgr.set({'title': title,
                          'description': description,
                          'url': url,
                          'credit': rights,
                          'uuid': uuid,
                          'content_type': content_type,
                          })

    @staticmethod
    def accepted_ct():
        """Return a list of content types accepted by the tile."""
        return ['Audio']

    @staticmethod
    def get_uuid(obj):
        return api.content.get_uuid(obj)

    def init_js(self):
        return """
$(document).ready(function() {{
    $('#audio_jplayer_{0}').audio_player({{'cssSelectorAncestor':'#audio_jpcontainer_{1}'}});
}});
""".format(self.id, self.id)
