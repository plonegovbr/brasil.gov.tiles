# -*- coding: utf-8 -*-
from Acquisition import aq_base
from brasil.gov.tiles import _ as _
from collective.cover.tiles.base import IPersistentCoverTile
from collective.cover.tiles.base import PersistentCoverTile
from collective.cover.tiles.configuration_view import IDefaultConfigureForm
from plone.autoform import directives as form
from plone.namedfile import field
from plone.namedfile import NamedBlobImage
from plone.tiles.interfaces import ITileDataManager
from Products.CMFPlone.utils import safe_hasattr
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.interface import implementer


class IBannerTile(IPersistentCoverTile):

    title = schema.TextLine(
        title=_(u'Title'),
        required=False,
    )

    image = field.NamedBlobImage(
        title=_(u'Image'),
        required=False,
    )

    form.no_omit('image_description')
    form.omitted(IDefaultConfigureForm, 'image_description')
    image_description = schema.TextLine(
        title=_(u'ALT'),
        required=False,
    )

    remote_url = schema.TextLine(
        title=_(u'URL'),
        required=False,
    )


@implementer(IBannerTile)
class BannerTile(PersistentCoverTile):

    index = ViewPageTemplateFile('templates/banner.pt')
    is_configurable = True
    is_editable = True
    is_droppable = True

    def accepted_ct(self):
        return ['Image', 'Link']

    def populate_with_object(self, obj):
        """Tile can be populated with images and links; in this case we're not
        going to take care of any modification of the original object; we just
        copy the data to the tile and deal with it.
        """
        if obj.portal_type not in self.accepted_ct():
            return

        super(BannerTile, self).populate_with_object(obj)  # check permissions
        obj = aq_base(obj)  # avoid acquisition
        title = obj.Title()
        rights = obj.Rights() if safe_hasattr(obj, 'Rights') else None

        # if image, store a copy of its data
        if obj.portal_type == 'Image':
            if safe_hasattr(obj, 'getImage'):
                data = obj.getImage().data
            else:
                data = obj.image.data
            image = NamedBlobImage(data)
        else:
            image = None
        image_description = obj.Description() or obj.Title()
        remote_url = obj.getRemoteUrl() if obj.portal_type == 'Link' else None

        data_mgr = ITileDataManager(self)
        data_mgr.set({
            'title': title,
            'image': image,
            'image_description': image_description,
            'remote_url': remote_url,
            'rights': rights,
        })

    def Title(self):
        return self.data.get('title', None)

    @property
    def Rights(self):
        return self.data.get('rights', None)

    @property
    def has_image(self):
        return self.data.get('image', None) is not None

    def getAlt(self):
        return self.data.get('image_description', None) or self.data.get('title', None)

    def getRemoteUrl(self):
        return self.data.get('remote_url', None)

    @property
    def is_empty(self):
        return not (self.Title() or self.has_image or self.getRemoteUrl())

    @property
    def css_class(self):
        tile_conf = self.get_tile_configuration()
        image_conf = tile_conf.get('image', None)
        if image_conf:
            css_class = image_conf['position']
            return css_class

    def thumbnail(self, scales):
        """Return a thumbnail of an image if the item has an image field and
        the field is visible in the tile.

        :param item: [required]
        :type item: content object
        """
        if self._field_is_visible('image'):
            tile_conf = self.get_tile_configuration()
            image_conf = tile_conf.get('image', None)
            if image_conf:
                scaleconf = image_conf['imgsize']
                if (scaleconf != '_original'):
                    # scale string is something like: 'mini 200:200'
                    scale = scaleconf.split(' ')[0]  # we need the name only: 'mini'
                else:
                    scale = None
                return scales.scale('image', scale)

    @property
    def htmltag(self):
        tile_conf = self.get_tile_configuration()
        title_conf = tile_conf.get('title', None)
        if title_conf:
            htmltag = title_conf['htmltag']
            return htmltag
