# -*- coding: utf-8 -*-
from Products.CMFPlone import interfaces as plone_interfaces
from Products.CMFQuickInstallerTool import interfaces as qi_interfaces
from zope.interface import implementer


PROJECTNAME = 'brasil.gov.tiles'


@implementer(qi_interfaces.INonInstallable)
class HiddenProducts(object):

    def getNonInstallableProducts(self):
        return [
            u'brasil.gov.tiles.upgrades.v2000',
            u'brasil.gov.tiles.upgrades.v3000',
            u'brasil.gov.tiles.upgrades.v4000',
            u'brasil.gov.tiles.upgrades.v4002',
        ]


@implementer(plone_interfaces.INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        return [
            u'brasil.gov.tiles:testfixture',
            u'brasil.gov.tiles:uninstall',
            u'brasil.gov.tiles:testfixture',
            u'brasil.gov.tiles.upgrades.v2000:default',
            u'brasil.gov.tiles.upgrades.v3000:default',
            u'brasil.gov.tiles.upgrades.v4000:default',
            u'brasil.gov.tiles.upgrades.v4002:default',
        ]
