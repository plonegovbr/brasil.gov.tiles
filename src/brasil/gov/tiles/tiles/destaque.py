# -*- coding: utf-8 -*-
from brasil.gov.tiles import _ as _
from collective.cover.tiles.list import IListTile
from collective.cover.tiles.list import ListTile
from plone.namedfile.field import NamedImage
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implementer


# XXX: we must refactor this tile
class IDestaqueTile(IListTile):

    # FIXME: Ver como migrar NamedImage para NamedBlobImage, como está previsto
    # em https://github.com/collective/collective.cover/blob/1.1b1/src/collective/cover/tiles/list.py#L66
    image = NamedImage(
        title=_(u'Image'),
        required=False,
        readonly=True,
    )


@implementer(IDestaqueTile)
class DestaqueTile(ListTile):

    index = ViewPageTemplateFile('templates/destaque.pt')

    is_editable = False
    limit = 2
    short_name = _(u'A highlight tile', default=u'A highlight tile')

    def thumbnail(self, item):
        if self._has_image_field(item):
            scales = item.restrictedTraverse('@@images')
            return scales.scale('image', 'mini')
