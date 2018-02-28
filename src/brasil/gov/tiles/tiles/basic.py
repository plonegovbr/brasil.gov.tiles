# -*- coding: utf-8 -*-
from brasil.gov.tiles import _ as _b
from collective.cover import _ as _
from collective.cover.controlpanel import ICoverSettings
from collective.cover.tiles.base import IPersistentCoverTile
from collective.cover.tiles.base import PersistentCoverTile
from collective.cover.tiles.configuration_view import IDefaultConfigureForm
from plone import api
from plone.autoform import directives as form
from plone.memoize import view
from plone.memoize.instance import memoizedproperty
from plone.namedfile.field import NamedBlobImage as NamedImage
from plone.registry.interfaces import IRegistry
from plone.tiles.interfaces import ITileDataManager
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.component import getUtility
from zope.interface import implementer


class IBasicTile(IPersistentCoverTile):

    title = schema.TextLine(
        title=_(u'Title'),
        required=False,
    )

    description = schema.Text(
        title=_(u'Description'),
        required=False,
    )

    image = NamedImage(
        title=_(u'Image'),
        required=False,
    )

    form.no_omit('image_description')
    form.omitted(IDefaultConfigureForm, 'image_description')
    image_description = schema.TextLine(
        title=_(u'ALT'),
        required=False,
    )

    form.omitted('date')
    form.no_omit(IDefaultConfigureForm, 'date')
    date = schema.Datetime(
        title=_(u'Date'),
        required=False,
        readonly=False,
    )

    form.omitted('subjects')
    form.no_omit(IDefaultConfigureForm, 'subjects')
    form.widget(subjects='z3c.form.browser.textarea.TextAreaFieldWidget')
    subjects = schema.Tuple(
        title=_(u'label_categories', default=u'Categories'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=(),
    )

    uuid = schema.TextLine(
        title=_(u'UUID'),
        required=False,
        readonly=True,
    )

    form.no_omit('variacao_titulo')
    form.omitted(IDefaultConfigureForm, 'variacao_titulo')
    variacao_titulo = schema.Choice(
        title=_b(u'Title Change'),
        values=(u'Normal',
                u'Grande',
                u'Gigante'),
        default=u'Normal',
        required=True,
    )


@implementer(IPersistentCoverTile)
class BasicTile(PersistentCoverTile):

    index = ViewPageTemplateFile('templates/basic.pt')

    is_configurable = True

    @memoizedproperty
    def brain(self):
        catalog = api.portal.get_tool('portal_catalog')
        uuid = self.data.get('uuid')
        result = catalog(UID=uuid) if uuid is not None else []
        assert len(result) <= 1
        return result[0] if result else None

    def Date(self):
        """ Return the date of publication of the original object; if it has
        not been published yet, it will return its modification date.
        """
        if self.brain is not None:
            return self.brain.Date

    def is_empty(self):
        return self.brain is None and \
            not [i for i in self.data.values() if i]

    def getURL(self):
        """ Return the URL of the original object.
        """
        if self.brain is not None:
            return self.brain.getURL()

    def Subject(self):
        """ Return the categories of the original object (AKA keywords, tags
            or labels).
        """
        if self.brain is not None:
            return self.brain.Subject

    def populate_with_object(self, obj):
        super(BasicTile, self).populate_with_object(obj)

        # initialize the tile with all fields needed for its rendering
        # note that we include here 'date' and 'subjects', but we do not
        # really care about their value: they came directly from the catalog
        # brain
        data = {
            'title': safe_unicode(obj.Title()),
            'description': safe_unicode(obj.Description()),
            # XXX: can we get None here? see below
            'uuid': api.content.get_uuid(obj),
            'date': True,
            'subjects': True,
            'image_description': safe_unicode(obj.Description()) or
            safe_unicode(obj.Title()),
        }

        # TODO: if a Dexterity object does not have the IReferenceable
        # behaviour enable then it will not work here
        # we need to figure out how to enforce the use of
        # plone.app.referenceablebehavior
        data_mgr = ITileDataManager(self)
        data_mgr.set(data)

    @view.memoize
    def accepted_ct(self):
        """
            Return a list with accepted content types ids
            basic tile accepts every content type
            allowed by the cover control panel

            this method is called for every tile in the compose view
            please memoize if you're doing some very expensive calculation
        """
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ICoverSettings)  # noqa
        return settings.searchable_content_types

    def getAlt(self):
        return (self.data.get('image_description', None) or
                self.data.get('title', None) or
                self.data.get('description', None))

    def variacao_titulo(self):
        tamanhos = {
            u'Normal': None,
            u'Grande': 'grande',
            u'Gigante': 'gigante',
        }
        if self.data['variacao_titulo']:
            return tamanhos[self.data['variacao_titulo']]
