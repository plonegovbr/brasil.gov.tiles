# -*- coding: utf-8 -*-
from brasil.gov.tiles.config import PROJECTNAME
from brasil.gov.tiles.testing import INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.browserlayer.utils import registered_layers
from plone.registry.interfaces import IRegistry
from Products.GenericSetup.upgrade import listUpgradeSteps
from zope.component import getUtility

import unittest


DEPENDENCIES = [
    'collective.cover',
    'collective.nitf',
    'collective.polls',
]
TILES = [
    'em_destaque',
    'nitf',
    'collective.polls',
    'destaque',
    'videogallery',
    'audio',
    'audiogallery',
    'mediacarousel',
    'social',
    'standaloneheader',
    'video',
    'banner_rotativo',
    'collective.cover.carousel',
]


class InstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING
    profile = 'brasil.gov.tiles:default'

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        self.st = self.portal['portal_setup']
        self.registry = getUtility(IRegistry)

    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME))

    def test_dependencies(self):
        for p in DEPENDENCIES:
            self.assertTrue(
                self.qi.isProductInstalled(p), '{0} not installed'.format(p))

    def test_browserlayer(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertIn('IBrasilGovTiles', layers, 'browser layer not installed')

    def test_tiles(self):
        registered_tiles = self.registry['plone.app.tiles']
        for tile in TILES:
            self.assertIn(tile, registered_tiles)

    def test_remove_collective_nitf_tile_on_install(self):
        registered_tiles = self.registry['plone.app.tiles']
        self.assertNotIn(u'collective.nitf', registered_tiles)

    def test_ultimo_upgrade_igual_metadata_xml_filesystem(self):
        """
        Testa se o número do último upgradeStep disponível é o mesmo do
        metadata.xml do profile.
        É também útil para garantir que para toda alteração feita no version
        do metadata.xml tenha um upgradeStep associado.
        Esse teste parte da premissa que o número dos upgradeSteps é sempre
        sequencial.
        """
        upgrade_info = self.qi.upgradeInfo(PROJECTNAME)
        upgradeSteps = listUpgradeSteps(self.st, self.profile, '')
        upgrades = [upgrade[0]['dest'][0] for upgrade in upgradeSteps]
        last_upgrade = sorted(upgrades, key=int)[-1]
        self.assertEqual(upgrade_info['installedVersion'],
                         last_upgrade)


class UninstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(
            self.qi.isProductInstalled(PROJECTNAME))

    def test_browserlayer_removed(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertNotIn('IBrasilGovTiles', layers,
                         'browser layer not removed')
