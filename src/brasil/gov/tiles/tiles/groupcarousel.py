# -*- coding: utf-8 -*-
from brasil.gov.tiles import _
from collective.cover.interfaces import ITileEditForm
from collective.cover.tiles.carousel import CarouselTile
from collective.cover.tiles.carousel import ICarouselTile
from plone.autoform import directives as form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.interface import implementer


class IGroupCarouselTile(ICarouselTile):
    """Display a carousel of items."""

    tile_description = schema.Text(title=_(u'Tile Description'), required=False)
    form.omitted('tile_description')
    form.no_omit(ITileEditForm, 'tile_description')

    switch_text = schema.TextLine(title=_(u'Switch Text'), required=False)
    form.omitted('switch_text')
    form.no_omit(ITileEditForm, 'switch_text')

    form.omitted('autoplay')


@implementer(IGroupCarouselTile)
class GroupCarouselTile(CarouselTile):
    """Display a carousel of items."""

    index = ViewPageTemplateFile('templates/groupcarousel.pt')
    short_name = _(u'msg_short_name_groupcarousel', default=u'Group Carousel')

    is_configurable = False
    is_droppable = True
    is_editable = True
    limit = 4 * 3

    @property
    def description(self):
        return self.data['tile_description']

    @property
    def switch_text(self):
        return self.data['switch_text']

    def populate_with_object(self, obj):
        """Add an object to the list of items
        :param obj: [required] The object to be added
        :type obj: Content object
        """
        self.populate_with_uuids([self.get_uuid(obj)])

    def results(self):
        """Return the list of objects stored in the tile."""
        page = []

        for i, item in enumerate(super(GroupCarouselTile, self).results(), start=1):
            page.append(item)
            if i % 4 == 0:
                yield page
                page = []
        if page:
            yield page

    def is_empty(self):
        """Check if the tile is empty."""
        return super(GroupCarouselTile, self).results() == []
