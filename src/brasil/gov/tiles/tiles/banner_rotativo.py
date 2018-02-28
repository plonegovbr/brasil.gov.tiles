# -*- coding: utf-8 -*-
from brasil.gov.tiles import _ as _
from collective.cover.tiles.configuration_view import IDefaultConfigureForm
from collective.cover.tiles.list import IListTile
from collective.cover.tiles.list import ListTile
from plone import api
from plone.autoform import directives as form
from plone.memoize import view
from plone.namedfile.field import NamedBlobImage as NamedImage
from plone.tiles.interfaces import ITileDataManager
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.interface import implementer


class IBannerRotativoTile(IListTile):
    """
    """

    form.omitted('header')
    form.no_omit(IDefaultConfigureForm, 'header')
    header = schema.TextLine(
        title=_(u'Header'),
        required=False,
        readonly=True,
    )

    form.omitted('title')
    form.no_omit(IDefaultConfigureForm, 'title')
    title = schema.TextLine(
        title=_(u'Title'),
        required=False,
        readonly=True,
    )

    form.omitted('description')
    form.no_omit(IDefaultConfigureForm, 'description')
    description = schema.Text(
        title=_(u'Description'),
        required=False,
        readonly=True,
    )

    form.omitted('date')
    form.no_omit(IDefaultConfigureForm, 'date')
    date = schema.Datetime(
        title=_(u'Date'),
        required=False,
        readonly=True,
    )

    form.omitted('image')
    form.no_omit(IDefaultConfigureForm, 'image')
    image = NamedImage(
        title=_(u'Image'),
        required=False,
        readonly=True,
    )

    layout = schema.Choice(
        title=u'Layout',
        values=(u'Banner',
                u'Chamada de foto',
                u'Texto sobreposto'),
        default=u'Banner',
        required=True,
    )

    form.omitted('uuids')
    form.no_omit(IDefaultConfigureForm, 'uuids')
    uuids = schema.Dict(
        title=_(u'Elements'),
        key_type=schema.TextLine(),
        value_type=schema.Dict(
            key_type=schema.TextLine(),
            value_type=schema.TextLine(),
        ),
        required=False,
    )


@implementer(IBannerRotativoTile)
class BannerRotativoTile(ListTile):

    index = ViewPageTemplateFile('templates/banner_rotativo.pt')
    is_configurable = False
    is_editable = True
    limit = 4

    def populate_with_object(self, obj):
        super(BannerRotativoTile, self).populate_with_object(obj)  # check permission
        if not self._has_image_field(obj):
            return
        self.set_limit()
        uuid = api.content.get_uuid(obj)
        title = obj.Title()
        description = obj.Description()
        rights = obj.Rights()
        data_mgr = ITileDataManager(self)
        old_data = data_mgr.get()
        if data_mgr.get()['uuids']:
            uuids = data_mgr.get()['uuids']
            if type(uuids) != list:
                uuids = [uuid]
            elif uuid not in uuids:
                uuids.append(uuid)

            uuids = uuids[:self.limit]
        else:
            uuids = [uuid]
        old_data['title'] = title
        old_data['description'] = description
        old_data['rights'] = rights
        data_mgr.set(old_data)
        self.populate_with_uuids(uuids)

    def thumbnail(self, item):
        """Return a thumbnail of an image if the item has an image field and
        the field is visible in the tile.

        :param item: [required]
        :type item: content object
        """
        if self._has_image_field(item):
            scales = item.restrictedTraverse('@@images')
            return scales.scale('image', width=750, height=423)

    @view.memoize
    def accepted_ct(self):
        results = ListTile.accepted_ct(self)
        results.append(u'ExternalContent')
        return results

    def layout_banner(self):
        if (self.data['layout'] == u'Banner' or self.data['layout'] is None):
            layout = 1
        elif (self.data['layout'] == u'Chamada de foto'):
            layout = 2
        else:
            layout = 3

        return layout

    def show_description(self):
        return (self.data['layout'] == u'Chamada de foto')

    def show_rights(self):
        return (self.data['layout'] == u'Chamada de foto' or self.data['layout'] == u'Texto sobreposto')

    def tile_class(self):
        if self.layout_banner() == 1:
            return 'chamada_sem_foto tile-content'
        elif self.layout_banner() == 2:
            return 'chamada_com_foto tile-content'
        else:
            return 'chamada_sobrescrito tile-content'

    def show_nav(self):
        return (len(self.results()) > 1)
