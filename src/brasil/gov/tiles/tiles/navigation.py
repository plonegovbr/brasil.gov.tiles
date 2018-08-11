# -*- coding: utf-8 -*-
from Acquisition import aq_parent
from brasil.gov.tiles import _
from collective.cover.tiles.base import IPersistentCoverTile
from collective.cover.tiles.base import PersistentCoverTile
from plone import api
from plone.dexterity.interfaces import IDexterityContent
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implementer


class INavigationTile(IPersistentCoverTile):
    """Display a navigation of items."""


@implementer(INavigationTile)
class NavigationTile(PersistentCoverTile):
    """Display a navigation of items."""

    index = ViewPageTemplateFile('templates/navigation.pt')
    short_name = _(u'msg_short_name_navigation', default=u'Navigation')

    is_configurable = False
    is_droppable = False
    is_editable = False

    def __init__(self, context, request):
        super(NavigationTile, self).__init__(context, request)
        self._setup()

    def _setup(self):
        self.menu_items = []
        self.session = aq_parent(self.context)
        try:
            for o in self.context.listFolderContents():
                if self._exclude_from_nav(o):
                    continue
                if api.content.get_state(o, '') != 'published':
                    continue
                self.menu_items.append(o)
        except AttributeError:
            pass

    def _exclude_from_nav(self, obj):
        """Check DX and AT way if is a menu item."""
        if obj is None:
            return True
        if IDexterityContent.providedBy(obj):
            try:
                # Dexterity
                exclude_from_nav = obj.exclude_from_nav
                if callable(exclude_from_nav):
                    return True
                return exclude_from_nav
            except AttributeError:
                pass
        else:
            try:
                # Archetypes
                return obj.getExcludeFromNav()
            except AttributeError:
                pass
        return True  # For some content type that can't be a Menu

    def first_items(self):
        return self.menu_items[:3]

    def more_items(self):
        return self.menu_items[3:]
