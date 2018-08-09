# -*- coding: utf-8 -*-
from brasil.gov.tiles import _
from collective.cover.tiles.base import IPersistentCoverTile
from collective.cover.tiles.base import PersistentCoverTile
from plone import api
from plone.namedfile import field
from plone.namedfile import NamedBlobImage
from plone.tiles.interfaces import ITileDataManager
from Products.CMFPlone.utils import safe_hasattr
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.interface import implementer


class IPOTDTile(IPersistentCoverTile):
    """This tile displays an outstanding photo selected daily."""

    title = schema.TextLine(
        title=_(u'Title'),
        required=False,
        default=u'',
    )

    description = schema.Text(
        title=_(u'Description'),
        required=False,
        default=u'',
    )

    photo_credits = schema.TextLine(
        title=_(u'Credits'),
        required=False,
        default=u'',
    )

    image = field.NamedBlobImage(
        title=_(u'Photo'),
        required=False,
    )

    uuid = schema.TextLine(
        title=u'UUID',
        required=False,
        readonly=True,
    )


@implementer(IPOTDTile)
class POTDTile(PersistentCoverTile):
    """This tile displays an outstanding photo selected daily."""

    index = ViewPageTemplateFile('templates/potd.pt')
    short_name = _(u'msg_short_name_potd', default=u'Photo of the Day')

    is_configurable = True
    is_editable = True
    is_droppable = True

    @staticmethod
    def accepted_ct():
        return ['Image']

    def populate_with_object(self, obj):
        super(POTDTile, self).populate_with_object(obj)

        if safe_hasattr(obj, 'getImage'):
            data = obj.getImage().data
        else:
            data = obj.image.data
        image = NamedBlobImage(data)

        data_mgr = ITileDataManager(self)
        data = data_mgr.get()
        data['title'] = obj.title
        data['description'] = obj.Description()
        data['image'] = image
        data['uuid'] = api.content.get_uuid(obj=obj)
        data['photo_credits'] = obj.Rights()

        data_mgr.set(data)

    @property
    def is_empty(self):
        return not self.has_image

    def getAlt(self):
        return self.data.get('description', None) or self.data.get('title', None)
