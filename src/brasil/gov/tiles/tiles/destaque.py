# -*- coding: utf-8 -*-
from brasil.gov.tiles import _ as _
from collective.cover.controlpanel import ICoverSettings
from collective.cover.interfaces import ICoverUIDsProvider
from collective.cover.tiles.list import IListTile
from collective.cover.tiles.list import ListTile
from plone.memoize import view
from plone.namedfile.field import NamedImage
from plone.registry.interfaces import IRegistry
from plone.uuid.interfaces import IUUID
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.component import getUtility
from zope.interface import implementer


# XXX: we must refactor this tile
class IDestaqueTile(IListTile):

    uuids = schema.Dict(
        title=_(u'Elements'),
        key_type=schema.TextLine(),
        value_type=schema.Dict(
            key_type=schema.TextLine(),
            value_type=schema.TextLine(),
        ),
        required=False,
    )

    title = schema.List(
        title=_(u'Title'),
        required=False,
        readonly=True,
    )

    description = schema.Text(
        title=_(u'Description'),
        required=False,
        readonly=True,
    )

    image = NamedImage(
        title=_(u'Image'),
        required=False,
        readonly=True,
    )


@implementer(IDestaqueTile)
class DestaqueTile(ListTile):

    index = ViewPageTemplateFile('templates/destaque.pt')

    is_configurable = True
    is_droppable = True
    is_editable = False
    limit = 2

    # XXX: are we using this function somewhere? remove?
    def get_uid(self, obj):
        return IUUID(obj, None)

    @view.memoize
    def accepted_ct(self):
        """
            Return a list with accepted content types ids
            basic tile accepts every content type
            allowed by the cover control panel

            this method is called for every tile in the compose view
            please memoize if you're doing some very expensive calculation
        """
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ICoverSettings)
        return settings.searchable_content_types

    def thumbnail(self, item):
        if self._has_image_field(item):
            scales = item.restrictedTraverse('@@images')
            return scales.scale('image', 'mini')


@implementer(ICoverUIDsProvider)
class CollectionUIDsProvider(object):

    def __init__(self, context):
        self.context = context

    def getUIDs(self):
        """ Return a list of UIDs of collection objects.
        """
        return [i.UID for i in self.context.queryCatalog()]


@implementer(ICoverUIDsProvider)
class FolderUIDsProvider(object):

    def __init__(self, context):
        self.context = context

    def getUIDs(self):
        """ Return a list of UIDs of collection objects.
        """
        return [i.UID for i in self.context.getFolderContents()]


@implementer(ICoverUIDsProvider)
class GenericUIDsProvider(object):

    def __init__(self, context):
        self.context = context

    def getUIDs(self):
        """ Return a list of UIDs of collection objects.
        """
        return [IUUID(self.context)]
