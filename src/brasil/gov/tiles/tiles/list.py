# -*- coding: utf-8 -*-
from brasil.gov.tiles import _ as _
from collections import OrderedDict
from collective.cover.controlpanel import ICoverSettings
from collective.cover.interfaces import ICoverUIDsProvider
from collective.cover.tiles.base import IPersistentCoverTile
from collective.cover.tiles.base import PersistentCoverTile
from collective.cover.tiles.configuration_view import IDefaultConfigureForm
from plone import api
from plone.app.uuid.utils import uuidToObject
from plone.autoform import directives as form
from plone.memoize import view
from plone.namedfile.field import NamedBlobImage as NamedImage
from plone.registry.interfaces import IRegistry
from plone.tiles.interfaces import ITileDataManager
from plone.tiles.interfaces import ITileType
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.component import getUtility
from zope.component import queryUtility
from zope.interface import implementer
from zope.schema import getFieldsInOrder


# XXX: we must refactor this tile
class IListTile(IPersistentCoverTile):

    header = schema.TextLine(
        title=_(u'Header'),
        required=False,
    )

    form.omitted('title')
    form.no_omit(IDefaultConfigureForm, 'title')
    title = schema.TextLine(
        title=_(u'Title'),
        required=False,
    )

    form.omitted('description')
    form.no_omit(IDefaultConfigureForm, 'description')
    description = schema.Text(
        title=_(u'Description'),
        required=False,
    )

    form.omitted('date')
    form.no_omit(IDefaultConfigureForm, 'date')
    date = schema.Datetime(
        title=_(u'Date'),
        required=False,
    )

    form.omitted('image')
    form.no_omit(IDefaultConfigureForm, 'image')
    image = NamedImage(
        title=_(u'Image'),
        required=False,
    )

    form.omitted('uuids')
    form.no_omit(IDefaultConfigureForm, 'uuids')
    uuids = schema.List(
        title=_(u'Elements'),
        value_type=schema.TextLine(),
        required=False,
    )


@implementer(IListTile)
class ListTile(PersistentCoverTile):

    index = ViewPageTemplateFile('templates/list.pt')

    is_configurable = True
    is_droppable = True
    is_editable = True
    limit = 5
    configured_fields = OrderedDict()

    def results(self):
        """ Return the list of objects stored in the tile.
        """
        self.configured_fields = self.get_configured_fields()
        self.set_limit()
        uuids = self.data.get('uuids', None)
        result = []
        if uuids:
            uuids = [uuids] if type(uuids) == str else uuids
            for uuid in uuids:
                obj = uuidToObject(uuid)
                if obj:
                    result.append(obj)
                else:
                    self.remove_item(uuid)
        return result[:self.limit]

    def is_empty(self):
        return self.results() == []

    # XXX: we could get rid of this fixing the tile's schema
    def set_limit(self):
        field = self.configured_fields.get('uuids', None)
        if field:
            self.limit = int(field.get('size', self.limit))

    def populate_with_object(self, obj):
        super(ListTile, self).populate_with_object(obj)  # check permission
        uuids = ICoverUIDsProvider(obj).getUIDs()
        if uuids:
            self.populate_with_uuids(uuids)

    def populate_with_uuids(self, uuids):
        self.set_limit()
        data_mgr = ITileDataManager(self)

        old_data = data_mgr.get()
        old_data['header'] = _(u'tile List Title')
        for uuid in uuids:
            if old_data['uuids']:
                if type(old_data['uuids']) != list:
                    old_data['uuids'] = [uuid]
                elif uuid not in old_data['uuids']:
                    old_data['uuids'].append(uuid)
            else:
                old_data['uuids'] = [uuid]

        data_mgr.set(old_data)

    def replace_with_objects(self, uuids):
        super(ListTile, self).replace_with_objects(uuids)  # check permission
        self.set_limit()
        data_mgr = ITileDataManager(self)
        old_data = data_mgr.get()
        if type(uuids) == list:
            old_data['uuids'] = [i for i in uuids][:self.limit]
        else:
            old_data['uuids'] = [uuids]

        data_mgr.set(old_data)

    # FIXME: Usado enquanto o tipo lista não é herdado do cover. Ver
    # https://github.com/plonegovbr/brasil.gov.tiles/blob/7419efc721e133e694526fcecf9c24531faa64ab/src/brasil/gov/tiles/tiles/banner_rotativo.py#L116
    # e
    # https://github.com/plonegovbr/brasil.gov.tiles/issues/145
    # Entenda que, apesar dele adicionar, aqui, um dicionário em old_data['uuids'],
    # em populate_with_object de vários tiles ele ainda usa uma lista, (exemplo:
    # https://github.com/plonegovbr/brasil.gov.tiles/blob/7419efc721e133e694526fcecf9c24531faa64ab/src/brasil/gov/tiles/tiles/banner_rotativo.py#L98)
    # pois é o jeito que o brasil.gov.tiles sempre funcionou. Isso é alterado para versões mais
    # novas do cover para usar um dicionário (ver por exemplo o commit)
    # https://github.com/collective/collective.cover/blob/00f25a5cd0926c0a9e0e343406537f8bb9cd96ec/src/collective/cover/tiles/list.py#L189)
    # e ainda está em estudo uma melhor forma sobre essa migração, como proposto em
    # https://github.com/plonegovbr/brasil.gov.tiles/pull/173
    def replace_with_uuids(self, uuids):
        """ Replaces the whole list of items with a new list of items
        :param uuids: The list of objects' UUIDs to be used
        :type uuids: List of strings
        """
        data_mgr = ITileDataManager(self)
        old_data = data_mgr.get()
        # Clean old data
        old_data['uuids'] = dict()
        data_mgr.set(old_data)
        # Repopulate with clean list
        self.populate_with_uuids(uuids)

    def remove_item(self, uuid):
        super(ListTile, self).remove_item(uuid)
        data_mgr = ITileDataManager(self)
        old_data = data_mgr.get()
        uuids = data_mgr.get()['uuids']
        if uuid in uuids:
            del uuids[uuids.index(uuid)]
        old_data['uuids'] = uuids
        data_mgr.set(old_data)

    # XXX: are we using this function somewhere? remove?
    def get_uuid(self, obj):
        return api.content.get_uuid(obj)

    # XXX: refactoring the tile's schema should be a way to avoid this
    def get_configured_fields(self):
        # Override this method, since we are not storing anything
        # in the fields, we just use them for configuration
        tileType = queryUtility(ITileType, name=self.__name__)
        conf = self.get_tile_configuration()

        fields = getFieldsInOrder(tileType.schema)

        results = OrderedDict()
        for name, obj in fields:
            field = {'title': obj.title}
            if name in conf:
                field_conf = conf[name]
                if ('visibility' in field_conf and field_conf['visibility'] == u'off'):
                    # If the field was configured to be invisible, then just
                    # ignore it
                    continue

                if 'htmltag' in field_conf:
                    # If this field has the capability to change its html tag
                    # render, save it here
                    field['htmltag'] = field_conf['htmltag']

                if 'imgsize' in field_conf:
                    field['scale'] = field_conf['imgsize']

                if 'size' in field_conf:
                    field['size'] = field_conf['size']

            results[name] = field

        return results

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
        """Return a thumbnail of an image if the item has an image field and
        the field is visible in the tile.

        :param item: [required]
        :type item: content object
        """
        if self._has_image_field(item) and self._field_is_visible('image'):
            tile_conf = self.get_tile_configuration()
            image_conf = tile_conf.get('image', None)
            if image_conf:
                scaleconf = image_conf['imgsize']
                if (scaleconf != '_original'):
                    # scale string is something like: 'mini 200:200'
                    scale = scaleconf.split(' ')[0]  # we need the name only: 'mini'
                else:
                    scale = None
                scales = item.restrictedTraverse('@@images')
                return scales.scale('image', scale)

    def show_header(self):
        return self._field_is_visible('header')


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
