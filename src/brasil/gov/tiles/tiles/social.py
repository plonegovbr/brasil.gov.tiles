# -*- coding: utf-8 -*-
from brasil.gov.tiles import _ as _
from collective.cover.tiles.base import IPersistentCoverTile
from collective.cover.tiles.base import PersistentCoverTile
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.PythonScripts.standard import url_quote
from zope import schema
from zope.interface import implementer


class ISocialTile(IPersistentCoverTile):

    wid = schema.TextLine(
        title=_(u'Twitter widget id'),
        required=False,
    )

    username = schema.TextLine(
        title=_(u'Twitter username'),
        required=False,
    )

    facebook_page = schema.TextLine(
        title=_(u'Facebook Page URL'),
        required=False,
    )

    number_of_columns = schema.Choice(
        title=_(u'Columns'),
        values=(
            u'1',
            u'2',
            u'3',
        ),
        required=True,
    )


@implementer(IPersistentCoverTile)
class SocialTile(PersistentCoverTile):

    index = ViewPageTemplateFile('templates/social.pt')
    is_configurable = False
    is_droppable = False
    is_editable = True

    def get_wid(self):
        return self.data['wid']

    def get_username(self):
        return self.data['username']

    def get_quoted_username(self):
        return url_quote(self.data['username'])

    def accepted_ct(self):
        return None

    def facebook_available(self):
        return self.data['facebook_page']

    def twitter_available(self):
        return self.data['username'] and self.data['wid']

    def get_columns_size(self):
        column1 = '720'
        column2 = '450'
        column3 = '220'

        column_size = 250
        c = self.data['number_of_columns']
        if c == '1':
            column_size = column1
        elif c == '2':
            column_size = column2
        elif c == '3':
            column_size = column3
        return column_size
