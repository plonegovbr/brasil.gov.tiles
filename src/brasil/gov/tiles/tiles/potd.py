# -*- coding: utf-8 -*-
from Acquisition import aq_base
from brasil.gov.tiles import _
from collective.cover.tiles.base import IPersistentCoverTile
from collective.cover.tiles.base import PersistentCoverTile
from plone import api
from plone.namedfile import field
from plone.namedfile import NamedBlobImage
from plone.tiles.interfaces import ITileDataManager
from Products.CMFPlone.utils import safe_unicode
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

        obj = aq_base(obj)
        title = obj.Title()
        rights = obj.Rights()
        description = obj.Description()
        img = obj.image.data
        uuid = api.content.get_uuid(obj)

        if img:
            data = obj.image.data
            image = NamedBlobImage(data)
        else:
            image = None

        data_mgr = ITileDataManager(self)
        data_mgr.set({
            'title': safe_unicode(title),
            'image': image,
            'description': safe_unicode(description),
            'photo_credits': safe_unicode(rights),
            'uuid': uuid,
        })

    @property
    def is_empty(self):
        return not self.has_image
