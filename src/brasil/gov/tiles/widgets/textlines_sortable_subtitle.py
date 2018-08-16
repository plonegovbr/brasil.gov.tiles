# -*- coding: utf-8 -*-
from collective.cover.utils import get_types_use_view_action_in_listings
from collective.cover.utils import uuidToObject
from collective.cover.widgets.textlinessortable import TextLinesSortableWidget
from Products.CMFPlone.utils import safe_unicode
from z3c.form import interfaces
from z3c.form import widget
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile

import six
import zope.interface


class TextLinesSortableSubtitleWidget(TextLinesSortableWidget):
    """ Widget for adding new keywords and autocomplete with the ones in the
    system.
    """

    klass = u'textlines-sortable-subtitle-widget'
    input_template = ViewPageTemplateFile('textlines_sortable_subtitle_input.pt')

    def get_custom_subtitle(self, uuid):
        """ Returns the custom Subtitle assigned to a specific item

        :param uuid: [required] The object's UUID
        :type uuid: string
        :returns: The custom Subtitle
        """
        # Try to get custom subtitle
        subtitle = u''
        uuids = self.context['uuids']
        values = [uuids[i] for i in uuids if i == uuid]
        if values:
            subtitle = values[0].get('custom_subtitle', u'')
        if subtitle:
            return subtitle
        # If didn't find, get object subtitle
        obj = uuidToObject(uuid)

        subtitle = getattr(obj, 'subtitle', None)
        if subtitle is None:
            return None
        return safe_unicode(subtitle)

    def extract(self):
        """ Extracts the data from the HTML form and returns it

        :returns: A dictionary with the information
        """
        values = self.request.get(self.name).splitlines()
        uuids = [i for i in values if i]
        results = dict()
        for index, uuid in enumerate(uuids):
            obj = uuidToObject(uuid)
            results[uuid] = {
                u'order': six.text_type(index),
            }
            custom_title = self.request.get(
                '{0}.custom_title.{1}'.format(self.name, uuid), '',
            )
            if (custom_title != u'' and
               custom_title != safe_unicode(obj.Title())):
                results[uuid][u'custom_title'] = six.text_type(custom_title)
            custom_subtitle = self.request.get(
                '{0}.custom_subtitle.{1}'.format(self.name, uuid), '',
            )
            subtitle = getattr(obj, 'subtitle', None)
            if (custom_subtitle != u'' and
               subtitle is not None and
               custom_subtitle != safe_unicode(subtitle)):
                results[uuid][u'custom_subtitle'] = six.text_type(custom_subtitle)
            custom_description = self.request.get(
                '{0}.custom_description.{1}'.format(self.name, uuid), '',
            )
            if (custom_description != u'' and
               custom_description != safe_unicode(obj.Description())):
                results[uuid][u'custom_description'] = six.text_type(custom_description)
            custom_url = self.request.get(
                '{0}.custom_url.{1}'.format(self.name, uuid), '',
            )
            url = obj.absolute_url()
            if obj.portal_type in get_types_use_view_action_in_listings():
                url += '/view'
            if (custom_url != u'' and
               custom_url != url):
                results[uuid][u'custom_url'] = six.text_type(custom_url)
        return results


@zope.interface.implementer(interfaces.IFieldWidget)
def TextLinesSortableSubtitleFieldWidget(field, request):
    """IFieldWidget factory for TextLinesWidget."""
    return widget.FieldWidget(field, TextLinesSortableSubtitleWidget(request))
