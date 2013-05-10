# -*- coding: utf-8 -*-

from collective.cover.tiles.base import IPersistentCoverTile
from collective.cover.tiles.base import PersistentCoverTile
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.interface import implements


class ISocialTile(IPersistentCoverTile):

    wid = schema.TextLine(
        title=u'Twitter widget id',
        required=True,
    )

    username = schema.TextLine(
        title=u'Twitter username',
        required=True,
    )

    def get_wid():
        """
        Get the stored widget id.
        """

    def get_username():
        """
        Get the stored username.
        """

    def accepted_ct():
        """
        Check wich content types are accepted.
        """


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
