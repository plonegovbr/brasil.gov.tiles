# -*- coding: utf-8 -*-

from brasil.gov.tiles.tiles.list import ListTile
from collective.cover import _
from collective.cover.tiles.base import IPersistentCoverTile
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.interface import implements


class IEmDestaqueTile(IPersistentCoverTile):

    uuids = schema.List(
        title=_(u'Elements'),
        value_type=schema.TextLine(),
        required=False,
    )

    title = schema.TextLine(
        title=_(u'Title'),
        required=False,
        readonly=True,
    )


class EmDestaqueTile(ListTile):

    implements(IEmDestaqueTile)

    index = ViewPageTemplateFile("templates/em_destaque.pt")

    is_configurable = True
    is_droppable = True
    is_editable = False
    limit = 5
