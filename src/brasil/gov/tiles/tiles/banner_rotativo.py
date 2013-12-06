# -*- coding: utf-8 -*-

from brasil.gov.tiles.tiles.list import IListTile
from brasil.gov.tiles.tiles.list import ListTile
from collective.cover import _
from collective.cover.tiles.configuration_view import IDefaultConfigureForm
from plone.autoform import directives as form
from plone.memoize import view
from plone.namedfile.field import NamedBlobImage as NamedImage
from plone.tiles.interfaces import ITileDataManager
from plone.uuid.interfaces import IUUID
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.interface import implements


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
        title=u"Layout",
        values=(u'Banner',
                u'Chamada de foto'),
        default=u'Banner',
        required=True,
    )

    form.omitted('uuids')
    form.no_omit(IDefaultConfigureForm, 'uuids')
    uuids = schema.List(
        title=_(u'Elements'),
        value_type=schema.TextLine(),
        required=False,
        readonly=True,
    )


class BannerRotativoTile(ListTile):
    implements(IBannerRotativoTile)

    index = ViewPageTemplateFile("templates/banner_rotativo.pt")
    is_configurable = False
    is_editable = True
    limit = 4

    def populate_with_object(self, obj):
        super(BannerRotativoTile, self).populate_with_object(obj)  # check permission
        try:
            scale = obj.restrictedTraverse('@@images').scale('image')
        except:
            scale = None
        if not scale:
            return
        self.set_limit()
        uuid = IUUID(obj, None)
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

            old_data['uuids'] = uuids[:self.limit]
        else:
            old_data['uuids'] = [uuid]
        old_data['title'] = title
        old_data['description'] = description
        old_data['rights'] = rights
        data_mgr.set(old_data)

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
        if self.data['layout'] is None:
            return True  # default value

        return (self.data['layout'] == u'Banner')

    def tile_class(self):
        if self.layout_banner():
            return 'chamada_sem_foto tile-content'
        else:
            return 'chamada_com_foto tile-content'

    def show_nav(self):
        return (len(self.results()) > 1)
