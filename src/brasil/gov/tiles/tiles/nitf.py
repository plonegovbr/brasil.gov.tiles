# -*- coding: utf-8 -*-

from brasil.gov.tiles import _
from collective.cover.tiles.basic import BasicTile
from collective.cover.tiles.basic import IBasicTile
from collective.prettydate.interfaces import IPrettyDate
from DateTime import DateTime
from plone.tiles.interfaces import ITileDataManager
from zope import schema
from zope.browserpage import ViewPageTemplateFile
from zope.component import getMultiAdapter
from zope.component import getUtility


class INITFBasicTile(IBasicTile):
    """A tile that shows general information about news articles.
    """

    pretty_date = schema.Bool(
        title=_(u'Pretty dates'),
        required=False,
    )

    subtitle = schema.Text(
        title=_(u'Subtitle'),
        required=False,
    )

    section = schema.Text(
        title=_(u'Section'),
        required=False,
    )


class NITFBasicTile(BasicTile):
    """A tile that shows general information about news articles.
    """

    index = ViewPageTemplateFile("templates/nitf.pt")

    def accepted_ct(self):
        return ['collective.nitf.content']

    def populate_with_object(self, obj):
        super(NITFBasicTile, self).populate_with_object(obj)

        data_mgr = ITileDataManager(self)
        data = data_mgr.get()
        data['subtitle'] = obj.subtitle
        data['section'] = obj.section
        data_mgr.set(data)

    # XXX: future use
    def _Date(self, item):
        """ Return the properly formatted publication date of the item or, if
        the item has not been published yet, its modification date.
        """
        if self.data.pretty_date:
            date_utility = getUtility(IPrettyDate)
            # date_utility expects DateTime object
            return date_utility.date(DateTime(item.Date()))
        else:
            utils = getMultiAdapter((self.context, self.request),
                                    name=u'plone')
            # toLocalizedTime expects str object; use date_format_long
            return utils.toLocalizedTime(item.Date(), True)
