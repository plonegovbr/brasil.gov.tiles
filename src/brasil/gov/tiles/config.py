# -*- coding: utf-8 -*-
from Products.CMFPlone import interfaces as plone_interfaces
from Products.CMFQuickInstallerTool import interfaces as qi_interfaces
from zope.interface import implementer


PROJECTNAME = 'brasil.gov.tiles'


@implementer(qi_interfaces.INonInstallable)
class HiddenProducts(object):

    @staticmethod
    def getNonInstallableProducts():
        return [
        ]


@implementer(plone_interfaces.INonInstallable)
class HiddenProfiles(object):

    @staticmethod
    def getNonInstallableProfiles():
        return [
            u'brasil.gov.tiles:testfixture',
            u'brasil.gov.tiles:uninstall',
        ]
