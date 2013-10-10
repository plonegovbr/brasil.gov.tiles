# -*- coding: utf-8 -*-

from collective.cover import _
from collective.cover.tiles.basic import BasicTile
from collective.cover.tiles.basic import IBasicTile
from collective.cover.tiles.configuration_view import IDefaultConfigureForm
from plone.autoform import directives as form
from plone.tiles.interfaces import ITileDataManager
from zope import schema
from zope.browserpage import ViewPageTemplateFile


class INITFBasicTile(IBasicTile):
    """A tile that shows general information about news articles.
    """

    subtitle = schema.Text(
        title=_(u'Subtitle'),
        required=False,
    )

    form.omitted('section')
    form.no_omit(IDefaultConfigureForm, 'section')
    section = schema.Text(
        title=_(u'Section'),
        required=False,
    )


class NITFBasicTile(BasicTile):
    """A tile that shows general information about news articles.
    """

    index = ViewPageTemplateFile("templates/nitf.pt")

    def accepted_ct(self):
        return ['collective.nitf.content']

    def populate_with_object(self, obj):
        super(NITFBasicTile, self).populate_with_object(obj)

        data_mgr = ITileDataManager(self)
        data = data_mgr.get()
        data['subtitle'] = obj.subtitle
        data['section'] = obj.section
        data_mgr.set(data)

    def thumbnail(self, field, scales):
        scale = field.get('scale', 'large')
        return scales.scale('image', scale)
