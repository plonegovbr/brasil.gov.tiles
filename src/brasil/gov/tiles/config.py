# -*- coding: utf-8 -*-
from Products.CMFPlone import interfaces as plone_interfaces
from Products.CMFQuickInstallerTool import interfaces as qi_interfaces
from zope.interface import implements

PROJECTNAME = 'brasil.gov.tiles'


class HiddenProducts(object):
    implements(qi_interfaces.INonInstallable)

    def getNonInstallableProducts(self):
        return [
            u'brasil.gov.tiles.upgrades.v2000',
            u'brasil.gov.tiles.upgrades.v3000'
        ]


class HiddenProfiles(object):
    implements(plone_interfaces.INonInstallable)

    def getNonInstallableProfiles(self):
        return [
            u'brasil.gov.tiles:testfixture',
            u'brasil.gov.tiles:uninstall',
            u'brasil.gov.tiles:testfixture',
            u'brasil.gov.tiles.upgrades.v2000:default',
            u'brasil.gov.tiles.upgrades.v3000:default'
        ]
