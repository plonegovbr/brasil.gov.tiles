# -*- coding: utf-8 -*-
from brasil.gov.tiles import _ as _
from collective.cover.tiles.configuration_view import IDefaultConfigureForm
from collective.cover.tiles.list import IListTile
from collective.cover.tiles.list import ListTile
from plone.autoform import directives as form
from plone.memoize import view
from plone.namedfile.field import NamedBlobImage as NamedImage
from plone.tiles.interfaces import ITileDataManager
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.interface import implementer

import pkg_resources


class IBannerRotativoTile(IListTile):
    """
    """

    # FIXME: Ver como migrar NamedImage para NamedBlobImage, como está previsto
    # em https://github.com/collective/collective.cover/blob/1.1b1/src/collective/cover/tiles/list.py#L66
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


@implementer(IBannerRotativoTile)
class BannerRotativoTile(ListTile):

    index = ViewPageTemplateFile('templates/banner_rotativo.pt')
    is_configurable = False
    short_name = _(u'Rotating Banner', default=u'Rotating Banner')
    limit = 4

    def populate_with_object(self, obj):
        super(BannerRotativoTile, self).populate_with_object(obj)  # check permission
        if not self._has_image_field(obj):
            return
        data_mgr = ITileDataManager(self)
        old_data = data_mgr.get()
        old_data['title'] = obj.Title()
        old_data['description'] = obj.Description()
        old_data['rights'] = obj.Rights()
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
        try:
            pkg_resources.get_distribution('brasil.gov.portal')
            results.append(u'ExternalContent')
        except pkg_resources.DistributionNotFound:
            pass
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
        return (
            self.data['layout'] == u'Chamada de foto' or
            self.data['layout'] == u'Texto sobreposto'
        )

    def tile_class(self):
        if self.layout_banner() == 1:
            return 'chamada_sem_foto tile-content'
        elif self.layout_banner() == 2:
            return 'chamada_com_foto tile-content'
        else:
            return 'chamada_sobrescrito tile-content'

    def show_nav(self):
        return (len(self.results()) > 1)
