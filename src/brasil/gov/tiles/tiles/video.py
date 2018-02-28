# -*- coding: utf-8 -*-
from brasil.gov.tiles import _ as _
from collective.cover.tiles.base import IPersistentCoverTile
from collective.cover.tiles.base import PersistentCoverTile
from plone import api
from plone.tiles.interfaces import ITileDataManager
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema


class IVideoTile(IPersistentCoverTile):
    """
    """

    title = schema.TextLine(
        title=_(u'Title'),
        required=False,
    )

    embed_code = schema.TextLine(
        title=_(u'Videos'),
        required=False,
        readonly=True,
    )

    url = schema.TextLine(
        title=_(u'Videos'),
        required=False,
        readonly=True,
    )

    uuids = schema.List(
        title=_(u'Videos'),
        value_type=schema.TextLine(),
        required=False,
        readonly=True,
    )


class VideoTile(PersistentCoverTile):
    index = ViewPageTemplateFile('templates/video.pt')
    is_configurable = False
    is_editable = True
    limit = 1

    def populate_with_object(self, obj):
        super(VideoTile, self).populate_with_object(obj)  # check permission

        # here we should check if the embeded item has its a video
        # XXX
        if obj.portal_type in self.accepted_ct():

            title = obj.Title()
            url = obj.absolute_url()
            uuid = api.content.get_uuid(obj)
            embed = obj.embed_html
            data_mgr = ITileDataManager(self)
            data_mgr.set({'title': title,
                          'url': url,
                          'uuid': uuid,
                          'embed_code': embed,
                          })

    def get_uuid(self, obj):
        return api.content.get_uuid(obj)

    def accepted_ct(self):
        """ Return a list of content types accepted by the tile.
        """
        return ['sc.embedder']
