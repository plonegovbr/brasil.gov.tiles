# -*- coding: utf-8 -*-
from brasil.gov.tiles import _ as _
from collective.cover.tiles.base import IPersistentCoverTile
from collective.cover.tiles.base import PersistentCoverTile
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.interface import implementer


class IEmbedTile(IPersistentCoverTile):

    embed = schema.Text(
        title=_(u'Embedding code'),
        required=False,
    )

    title = schema.TextLine(
        title=_(u'Title'),
        required=False,
    )

    description = schema.Text(
        title=_(u'Description'),
        required=False,
    )


@implementer(IEmbedTile)
class EmbedTile(PersistentCoverTile):
    index = ViewPageTemplateFile('templates/embed.pt')

    is_configurable = True
    is_editable = True
    is_droppable = False

    def is_empty(self):
        return not (self.data.get('embed', None) or
                    self.data.get('title', None) or
                    self.data.get('description', None))

    def at_compose_tab(self):
        """Check if you are at compose tab
        """
        # Get parent request
        last_url = self.request['PATH_TRANSLATED']
        # Get last item
        last_url = last_url.split('/')[-1]
        return (last_url == 'compose')
