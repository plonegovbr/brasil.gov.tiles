# -*- coding: utf-8 -*-
from brasil.gov.tiles import _ as _
from brasil.gov.tiles.tiles.basic import BasicTile
from brasil.gov.tiles.tiles.basic import IBasicTile
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

    form.no_omit('variacao_titulo')
    form.omitted(IDefaultConfigureForm, 'variacao_titulo')
    variacao_titulo = schema.Choice(
        title=_(u'Change in Title'),
        values=(u'Normal',
                u'Grande',
                u'Gigante'),
        default=u'Normal',
        required=True,
    )


class NITFBasicTile(BasicTile):
    """A tile that shows general information about news articles.
    """

    index = ViewPageTemplateFile('templates/nitf.pt')

    def accepted_ct(self):
        return ['collective.nitf.content']

    def populate_with_object(self, obj):
        super(NITFBasicTile, self).populate_with_object(obj)

        data_mgr = ITileDataManager(self)
        data = data_mgr.get()
        data['subtitle'] = obj.subtitle
        data['section'] = obj.section
        img = obj.getImage()
        if img:
            data['image_description'] = img.Description() or img.Title()
        data_mgr.set(data)

    def thumbnail(self, field, scales):
        scale = field.get('scale', 'large')
        return scales.scale('image', scale)

    def variacao_titulo(self):
        tamanhos = {
            u'Normal': None,
            u'Grande': 'grande',
            u'Gigante': 'gigante'
        }
        if self.data['variacao_titulo']:
            return tamanhos[self.data['variacao_titulo']]
