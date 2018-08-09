# -*- coding: utf-8 -*-
from plone.namedfile.browser import Download
from plone.namedfile.utils import set_headers
from zope.publisher.interfaces import NotFound


class DownloadView(Download):

    def _getFile(self):
        if not self.fieldname:
            raise NotFound(self, '', self.request)
        else:
            data = self.context.data[self.fieldname]
            if data:
                filename = self.filename and self.filename or 'Download'
                set_headers(data, self.request.response, filename)
            else:
                raise NotFound(self, None, self.request)
        return data
