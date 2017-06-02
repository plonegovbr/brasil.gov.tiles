# -*- coding: utf-8 -*-
from AccessControl import Unauthorized
from brasil.gov.tiles import _ as _
from collective.cover.tiles.base import IPersistentCoverTile
from collective.cover.tiles.base import PersistentCoverTile
from collective.polls.polls import IPolls
from plone import api
from plone.app.uuid.utils import uuidToObject
from plone.tiles.interfaces import ITileDataManager
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import queryUtility
from zope.schema import TextLine


class IPollTile(IPersistentCoverTile):

    uuid = TextLine(
        title=_(u'Poll uuid'),
        readonly=True,
    )


class PollTile(PersistentCoverTile):

    index = ViewPageTemplateFile('templates/poll.pt')

    is_configurable = False

    def results(self):
        uuid = self.data.get('uuid', None)
        if uuid is not None:
            obj = uuidToObject(uuid)
            return obj

    @property
    def utility(self):
        utility = queryUtility(IPolls, name='collective.polls')
        return utility

    def poll(self):
        utility = self.utility
        uuid = self.data.get('uuid', None)
        poll = None
        if uuid is not None:
            poll = utility.poll_by_uuid(uuid)
        if not poll:
            # if we have no open poll, try closed ones
            results = utility.recent_polls(show_all=True,
                                           limit=1,
                                           review_state='closed')
            poll = results and results[0].getObject() or None
        return poll

    def getVotingResults(self):
        poll = self.poll()
        if poll.show_results:
            return poll.getResults()
        else:
            return None

    @property
    def can_vote(self):

        utility = self.utility
        poll = self.poll()
        if poll:
            try:
                return utility.allowed_to_vote(poll, self.request)
            except Unauthorized:
                return False
        return False

    @property
    def available(self):
        utility = self.utility
        poll = self.poll()
        if poll:
            can_view = utility.allowed_to_view(poll)
            # Do not show this portlet in the poll context
            return can_view and not (poll == self.context)
        return False

    def populate_with_object(self, obj):
        super(PollTile, self).populate_with_object(obj)

        uuid = api.content.get_uuid(obj)
        data_mgr = ITileDataManager(self)
        data_mgr.set({'uuid': uuid})

    def poll_uuid(self):
        utility = self.utility
        return utility.uuid_for_poll(self.poll())

    def delete(self):
        data_mgr = ITileDataManager(self)
        data_mgr.delete()

    def accepted_ct(self):
        valid_ct = ['collective.polls.poll']
        return valid_ct

    def has_data(self):
        uuid = self.data.get('uuid', None)
        return uuid is not None

    def is_closed(self):
        state = 'closed'
        if self.poll():
            state = api.content.get_state(self.poll())
        return state == 'closed'
