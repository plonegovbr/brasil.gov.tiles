# -*- coding: utf-8 -*-
from brasil.gov.tiles import _ as _
from brasil.gov.tiles.tiles.list import IListTile
from brasil.gov.tiles.tiles.list import ListTile
from collective.cover.widgets.textlinessortable import TextLinesSortableFieldWidget
from plone.autoform import directives as form
from plone.tiles.interfaces import ITileDataManager
from plone.uuid.interfaces import IUUID
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.interface import implementer


class ICarouselTile(IListTile):
    """
    """

    autoplay = schema.Bool(
        title=_(u'Auto play'),
        required=False,
        default=True,
    )

    form.widget(uuids=TextLinesSortableFieldWidget)
    uuids = schema.List(
        title=_(u'Elements'),
        value_type=schema.TextLine(),
        required=False,
        readonly=False,
    )


@implementer(ICarouselTile)
class CarouselTile(ListTile):

    index = ViewPageTemplateFile('templates/carousel.pt')
    is_configurable = True
    is_editable = True

    def populate_with_object(self, obj):
        super(CarouselTile, self).populate_with_object(obj)  # check permission
        if not self._has_image_field(obj):
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

    def autoplay(self):
        if self.data['autoplay'] is None:
            return True  # default value

        return self.data['autoplay']

    def init_js(self):
        return """
$(function() {{
    Galleria.loadTheme("++resource++collective.cover/galleria-theme/galleria.cover_theme.js");
    Galleria.run('#galleria-{0} .galleria-inner');

    if($('body').hasClass('template-view')) {{
        Galleria.configure({{ autoplay: {1} }});
    }};
}});
""".format(self.id, str(self.autoplay()).lower())
