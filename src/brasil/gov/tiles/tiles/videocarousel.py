# -*- coding: utf-8 -*-
from collective.cover import _
from collective.cover.interfaces import ITileEditForm
from collective.cover.tiles.carousel import CarouselTile
from collective.cover.tiles.list import IListTile
from collective.cover.widgets.textlinessortable import TextLinesSortableFieldWidget
from plone.autoform import directives as form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.interface import implementer


class IVideoCarouselTile(IListTile):
    """A tile that shows a carousel of videos."""

    tile_description = schema.Text(title=_(u'Tile Description'), required=False)
    form.omitted('tile_description')
    form.no_omit(ITileEditForm, 'tile_description')

    switch_text = schema.TextLine(title=_(u'Switch Text'), required=False)
    form.omitted('switch_text')
    form.no_omit(ITileEditForm, 'switch_text')

    form.no_omit(ITileEditForm, 'uuids')
    form.widget(uuids=TextLinesSortableFieldWidget)


@implementer(IVideoCarouselTile)
class VideoCarouselTile(CarouselTile):
    """A tile that shows a carousel of videos."""

    index = ViewPageTemplateFile('templates/videocarousel.pt')
    is_configurable = True
    is_droppable = True
    is_editable = True
    short_name = _(u'msg_short_name_video_carousel', default=u'Video Carousel')

    @staticmethod
    def accepted_ct():
        return ['sc.embedder']

    @property
    def tile_description(self):
        return self.data['tile_description']

    @property
    def switch_text(self):
        return self.data['switch_text']

    def results(self):
        """Return the tile items paginated

        :yields: A list with 3 items to be inserted
        """
        page = []

        for i, item in enumerate(super(VideoCarouselTile, self).results()):
            page.append(item)
            if (i + 1) % 3 == 0:
                yield page
                page = []
        if page:
            yield page

    def is_empty(self):
        """Check if the tile is empty."""
        return super(VideoCarouselTile, self).results() == []
