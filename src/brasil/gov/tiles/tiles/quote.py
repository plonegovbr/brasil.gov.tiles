# -*- coding: utf-8 -*-
from brasil.gov.tiles import _
from collective.cover.interfaces import ITileEditForm
from collective.nitf.tiles.nitf import INITFTile
from collective.nitf.tiles.nitf import NITFTile
from plone import api
from plone.autoform import directives as form
from plone.tiles.interfaces import ITileDataManager
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.interface import implementer
from zope.schema import Choice
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class IQuoteTile(INITFTile):
    """A tile that shows an article quote."""

    form.omitted('quote_color')
    form.no_omit(ITileEditForm, 'quote_color')
    quote_color = Choice(
        title=_(u'Quote color'),
        vocabulary=SimpleVocabulary([
            SimpleTerm(value=u'blue', title=_(u'Blue')),
            SimpleTerm(value=u'green', title=_(u'Green')),
        ]),
        required=True,
        default=u'blue',
    )

    form.omitted('quote')
    form.no_omit(ITileEditForm, 'quote')
    quote = schema.Text(
        title=_(u'Quote'),
        required=False,
    )

    form.omitted('quote_rights')
    form.no_omit(ITileEditForm, 'quote_rights')
    quote_rights = schema.TextLine(
        title=_(u'Quote Rights'),
        required=False,
    )


@implementer(IQuoteTile)
class QuoteTile(NITFTile):
    """A tile that shows an article quote."""

    index = ViewPageTemplateFile('templates/quote.pt')
    short_name = _(u'msg_short_name_quote', u'Quote')

    def populate_with_object(self, obj):
        image = obj.image()

        data_mgr = ITileDataManager(self)
        data = data_mgr.get()
        data['title'] = obj.title
        data['description'] = obj.description
        data['subtitle'] = obj.subtitle
        data['section'] = obj.section
        data['uuid'] = api.content.get_uuid(obj=obj)
        data['date'] = True
        data['subjects'] = True
        data['image'] = self.get_image_data(image)
        data['media_producer'] = obj.media_producer()

        # clear scales as new image is getting saved
        self.clear_scales()
        data_mgr.set(data)

    def color_class(self):
        color = self.data.get('quote_color')
        if color is None:
            return u'quote-blue'  # default value
        return u'quote-' + color

    def quote(self):
        return self.data.get('quote', '')

    def quote_rights(self):
        return self.data.get('quote_rights', '')
