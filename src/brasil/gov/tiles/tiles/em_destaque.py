# -*- coding: utf-8 -*-
from brasil.gov.tiles import _ as _
from brasil.gov.tiles.tiles.list import ListTile
from collective.cover.tiles.base import IPersistentCoverTile
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.interface import implementer

import warnings


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


@implementer(IEmDestaqueTile)
class EmDestaqueTile(ListTile):

    index = ViewPageTemplateFile('templates/em_destaque.pt')

    is_configurable = True
    is_droppable = True
    is_editable = False
    limit = 5

    def __call__(self):
        path = '/'.join(self.context.getPhysicalPath())
        msg = ('Use of tile "Em destaque" is deprecated '
               'and will be removed for the next version {0}'.format(path))
        warnings.warn(msg, DeprecationWarning)
        return self.index()
