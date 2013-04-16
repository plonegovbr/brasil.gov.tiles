# -*- coding: utf-8 -*-

from collective.cover.tiles.base import IPersistentCoverTile
from collective.cover.tiles.base import PersistentCoverTile
from plone.tiles.interfaces import ITileDataManager
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.interface import implements


class ITwitterTile(IPersistentCoverTile):

    wid = schema.TextLine(
        title=u'Twitter widget id',
        required=True,
    )

    username = schema.TextLine(
        title=u'Twitter username',
        required=True,
    )

<<<<<<< HEAD
=======
    def delete():
        """
        This method removes the persistent data created for this tile
        """

>>>>>>> * Added credits.
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


class TwitterTile(PersistentCoverTile):

    index = ViewPageTemplateFile("templates/twitter.pt")
    implements(IPersistentCoverTile)
    is_configurable = False
    is_droppable = False
    is_editable = True

    def get_wid(self):
        return self.data['wid']

    def get_username(self):
        return self.data['username']

<<<<<<< HEAD
=======
    def delete(self):
        data_mgr = ITileDataManager(self)
        data_mgr.delete()

>>>>>>> * Added credits.
    def accepted_ct(self):
        return None
