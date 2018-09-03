# -*- coding: utf-8 -*-
from brasil.gov.tiles import _
from collective.cover.tiles.base import IPersistentCoverTile
from collective.cover.tiles.base import PersistentCoverTile
from plone import api
from plone.namedfile import field
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

        title = safe_unicode(obj.Title())
        description = safe_unicode(obj.Description())
        rights = safe_unicode(obj.Rights())

        image = self.get_image_data(obj)
        if image:
            # clear scales if new image is getting saved
            self.clear_scales()

        data = {
            'title': title,
            'description': description,
            'uuid': api.content.get_uuid(obj=obj),
            'image': image,
            'photo_credits': rights,
            # FIXME: https://github.com/collective/collective.cover/issues/778
            'alt_text': description or title,
        }

        data_mgr = ITileDataManager(self)
        data_mgr.set(data)

    @property
    def is_empty(self):
        return not self.has_image

    def getAlt(self):
        return self.data.get('description', None) or self.data.get('title', None)
