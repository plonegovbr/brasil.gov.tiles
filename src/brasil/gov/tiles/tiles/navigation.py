# -*- coding: utf-8 -*-
from Acquisition import aq_parent
from brasil.gov.tiles import _
from collective.cover.tiles.base import IPersistentCoverTile
from collective.cover.tiles.base import PersistentCoverTile
from plone import api
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implementer


class INavigationTile(IPersistentCoverTile):
    """Display a section navigation."""


@implementer(INavigationTile)
class NavigationTile(PersistentCoverTile):
    """Display a section navigation."""

    index = ViewPageTemplateFile('templates/navigation.pt')
    short_name = _(u'msg_short_name_navigation', default=u'Navigation')

    is_configurable = False
    is_droppable = False
    is_editable = False

    def __call__(self):
        self.setup()
        return self.index()

    def setup(self):
        self.menu_items = []
        self.section = aq_parent(self.context)

        results = api.content.find(
            context=self.section, depth=1, review_state='published')

        for item in results:
            if not item.exclude_from_nav:
                self.menu_items.append(item)

    def first_items(self):
        return self.menu_items[:3]

    def more_items(self):
        return self.menu_items[3:]
