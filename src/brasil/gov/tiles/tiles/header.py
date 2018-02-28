# -*- coding: utf-8 -*-
from brasil.gov.tiles import _ as _
from collective.cover.tiles.base import IPersistentCoverTile
from collective.cover.tiles.base import PersistentCoverTile
from plone import api
from plone.tiles.interfaces import ITileDataManager
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.interface import implementer


class IHeaderTile(IPersistentCoverTile):

    title = schema.TextLine(
        title=_(u'Title'),
        required=False,
    )

    link_text = schema.TextLine(
        title=_(u'Link text'),
        required=False,
    )

    link_url = schema.TextLine(
        title=_(u'Link url'),
        required=False,
    )

    link_boolean = schema.Bool(
        title=_(u'Title as link?'),
        required=False,
    )

    uuid = schema.TextLine(
        title=_(u'UUID'),
        required=False,
        readonly=True,
    )


@implementer(IPersistentCoverTile)
class HeaderTile(PersistentCoverTile):

    index = ViewPageTemplateFile('templates/header.pt')
    is_configurable = True
    is_droppable = True
    is_editable = True

    def populate_with_object(self, obj):
        super(HeaderTile, self).populate_with_object(obj)  # check permissions

        title = obj.Title()
        url = obj.absolute_url()
        try:
            link_boolean = obj.link_boolean
        except AttributeError:
            link_boolean = False
        link_text = title
        data_mgr = ITileDataManager(self)
        uuid = api.content.get_uuid(obj)
        data_mgr.set({'title': title,
                      'link_url': url,
                      'link_text': link_text,
                      'link_boolean': link_boolean,
                      'uuid': uuid,
                      })
