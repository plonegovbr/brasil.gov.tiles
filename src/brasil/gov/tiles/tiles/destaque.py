# -*- coding: utf-8 -*-
from brasil.gov.tiles import _ as _
from collective.cover.controlpanel import ICoverSettings
from collective.cover.interfaces import ICoverUIDsProvider
from collective.cover.tiles.list import IListTile
from collective.cover.tiles.list import ListTile
from plone import api
from plone.memoize import view
from plone.namedfile.field import NamedImage
from plone.registry.interfaces import IRegistry
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
    short_name = _(u'A highlight tile', default=u'A highlight tile')

    # FIXME: Até a versão 1.4b1 de collective.cover, o funcionamento da lista
    # do collective.cover e do brasil.gov.tiles, apesar de uma diferença ou outra
    # bem pontual, eram bem similares. A partir da 1.5b1, devido ao PR
    # https://github.com/collective/collective.cover/pull/714,
    # a forma de tratar diretórios e coleções mudou de forma drástica nos tiles
    # mas ainda não estamos preparados para essa mudança (pois os demais tiles
    # ainda herdam do ListTile de brasil.gov.tiles).
    # Como ainda iremos atender ao PR
    # https://github.com/plonegovbr/brasil.gov.tiles/pull/173 que irá resolver
    # isso de forma definitiva, iremos redefinir os métodos que funcionavam ok
    # na 1.1b1 mas que foram alterados no 1.5b1 para manter esse tile com o
    # mesmo comportamento dos demais em brasil.gov.tiles.
    def populate_with_object(self, obj):
        """ Add an object to the list of items

        :param obj: [required] The object to be added
        :type obj: Content object
        """
        super(ListTile, self).populate_with_object(obj)  # check permission
        uuids = ICoverUIDsProvider(obj).getUIDs()
        if uuids:
            self.populate_with_uuids(uuids)

    # FIXME: Com a atualização para 1.1b1 e 1.6b1, esse método pode ser removido.
    # Avaliar e testar durante o PR
    # https://github.com/plonegovbr/brasil.gov.tiles/pull/173
    # XXX: are we using this function somewhere? remove?
    def get_uuid(self, obj):
        return api.content.get_uuid(obj)

    # FIXME: Com a atualização para 1.1b1 e 1.6b1, esse método pode ser removido.
    # Avaliar e testar durante o PR
    # https://github.com/plonegovbr/brasil.gov.tiles/pull/173
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
        settings = registry.forInterface(ICoverSettings)  # noqa
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
        return [api.content.get_uuid(self.context)]
