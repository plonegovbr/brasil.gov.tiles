# -*- coding: utf-8 -*-
from brasil.gov.tiles import _ as _
from collective.cover.tiles.list import IListTile
from collective.cover.tiles.list import ListTile
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implementer


class IEmDestaqueTile(IListTile):
    """"""


@implementer(IEmDestaqueTile)
class EmDestaqueTile(ListTile):

    index = ViewPageTemplateFile('templates/em_destaque.pt')

    is_editable = False
    short_name = _(u'Featured', default=u'Featured')
