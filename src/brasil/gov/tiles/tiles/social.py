# -*- coding: utf-8 -*-

from collective.cover.tiles.base import IPersistentCoverTile
from collective.cover.tiles.base import PersistentCoverTile
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.interface import implements


class ISocialTile(IPersistentCoverTile):

    wid = schema.TextLine(
        title=u'Twitter widget id',
        required=False,
    )

    username = schema.TextLine(
        title=u'Twitter username',
        required=False,
    )

    facebook_page = schema.TextLine(
        title=u'Facebook Page URL',
        required=False,
    )


class SocialTile(PersistentCoverTile):

    index = ViewPageTemplateFile("templates/social.pt")
    implements(IPersistentCoverTile)
    is_configurable = False
    is_droppable = False
    is_editable = True

    def get_wid(self):
        return self.data['wid']

    def get_username(self):
        return self.data['username']

    def accepted_ct(self):
        return None

    def facebook_available(self):
        return self.data['facebook_page']

    def twitter_available(self):
        return self.data['username'] and self.data['wid']
