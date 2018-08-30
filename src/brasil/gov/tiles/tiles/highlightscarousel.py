# -*- coding: utf-8 -*-
from brasil.gov.tiles import _
from collective.cover.interfaces import ITileEditForm
from collective.cover.tiles.carousel import CarouselTile
from collective.cover.tiles.carousel import ICarouselTile
from plone.autoform import directives as form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.interface import implementer


class IHighlightsCarousel(ICarouselTile):
    """Display a carousel of items."""

    tile_description = schema.Text(title=_(u'Tile Description'), required=False)
    form.omitted('tile_description')
    form.no_omit(ITileEditForm, 'tile_description')

    form.omitted('autoplay')


@implementer(IHighlightsCarousel)
class HighlightsCarousel(CarouselTile):
    """Display a carousel of items."""

    index = ViewPageTemplateFile('templates/highlightscarousel.pt')
    short_name = _(u'msg_short_name_highlightscarousel', default=u'Highlights Carousel')

    is_configurable = False
    is_droppable = True
    is_editable = True
    limit = 5 * 3

    @property
    def tile_description(self):
        return self.data['tile_description']
