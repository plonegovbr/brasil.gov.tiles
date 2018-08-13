# -*- coding: utf-8 -*-
from Acquisition import aq_parent
from brasil.gov.tiles import _
from collective.cover.tiles.base import IPersistentCoverTile
from collective.cover.tiles.base import PersistentCoverTile
from plone import api
from Products.CMFPlone.interfaces import IPloneSiteRoot
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
        self._setup()
        return self.render()

    def render(self):
        return self.index()

    def _setup(self):
        self.menu_items = []
        context = self.context
        if not IPloneSiteRoot.providedBy(self.context):
            context = aq_parent(self.context)

        self.section = context
        items = api.content.find(context=context,
                                 depth=1,
                                 exclude_from_nav='False',
                                 review_state='published')
        for item in items:
            self.menu_items.append(item)

    def first_items(self):
        return self.menu_items[:3]

    def more_items(self):
        return self.menu_items[3:]
