# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.cover import _
from collective.cover.tiles.configuration_view import IDefaultConfigureForm
from collective.cover.tiles.list import IListTile
from collective.cover.tiles.list import ListTile
from collective.cover.widgets.textlinessortable import TextLinesSortableFieldWidget
from plone.autoform import directives as form
from plone.memoize import view
from plone.namedfile.field import NamedBlobImage as NamedImage
from plone.tiles.interfaces import ITileDataManager
from plone.uuid.interfaces import IUUID
from zope import schema
from zope.interface import implements


class IBannerRotativoTile(IListTile):
    """
    """

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
    is_configurable = True
    is_editable = False
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
        data_mgr.set(old_data)

    def scale(self, item):
        scales = item.restrictedTraverse('@@images')
        try:
            return scales.scale('image', width=766, height=248)
        except:
            return None

    @view.memoize
    def accepted_ct(self):
        results = ListTile.accepted_ct(self)
        results.append(u'ExternalContent')
        return results
