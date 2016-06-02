# -*- coding: utf-8 -*-
from brasil.gov.tiles.config import PROJECTNAME
from brasil.gov.tiles.testing import INTEGRATION_TESTING
from collective.cover.tests.test_upgrades import Upgrade9to10TestCase
from collective.cover.tests.test_upgrades import UpgradeTestCaseBase
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.browserlayer.utils import registered_layers
from plone.registry.interfaces import IRegistry
from plone.tiles.interfaces import ITileDataManager
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
    'poll',
    'destaque',
    'videogallery',
    'audio',
    'audiogallery',
    'mediacarousel',
    'social',
    'standaloneheader',
    'video',
    'banner_rotativo',
]


class InstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']

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
        self.registry = getUtility(IRegistry)
        registered_tiles = self.registry['plone.app.tiles']
        for tile in TILES:
            self.assertIn(tile, registered_tiles)


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


class Upgrade3000to4000TestCase(Upgrade9to10TestCase):

    """
    Essa classe de testes herda de Upgrade9to10TestCase, de collective.cover,
    por ser o mesmo teste de novos uuids e por conter métodos de chamar
    upgradeSteps. collective.cover já é dependência de brasil.gov.tiles.
    brasil.gov.portal também possui métodos semelhantes que tratam de
    upgradeSteps mas não é dependência.
    """

    layer = INTEGRATION_TESTING

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'3000', u'4000')
        self.profile_id = u'brasil.gov.tiles:default'

    def test_upgrade_to_10_registrations(self):
        # XXX: Como herdo de Upgrade9to10TestCase mas possuo dois upgradeSteps
        # esse método dá erro, mas não preciso dele.
        pass

    def test_upgrade_to_4000_registrations(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertTrue(int(version) >= int(self.to_version))
        self.assertEqual(self._how_many_upgrades_to_do(), 2)

    def test_new_uuids_structure(self):
        title = u'Atualiza estrutura no banco do tipo Destaque'
        step = self._get_upgrade_step(title)
        self.assertIsNotNone(step)

        # simulate state on previous version
        cover = self._create_cover('test-cover', 'Empty layout')
        cover.cover_layout = (
            '[{"type": "row", "children": [{"column-size": 16, "type": '
            '"group", "children": [{"tile-type": '
            '"destaque", "type": "tile", "id": '
            '"ca6ba6675ef145e4a569c5e410af7511"}], "roles": ["Manager"]}]}]'
        )

        tile = cover.get_tile('ca6ba6675ef145e4a569c5e410af7511')
        old_data = ITileDataManager(tile).get()
        old_data['uuids'] = ['uuid1', 'uuid3', 'uuid2']
        ITileDataManager(tile).set(old_data)

        # run the upgrade step to validate the update
        self._do_upgrade_step(step)
        old_data = ITileDataManager(tile).get()
        self.assertFalse(isinstance(old_data['uuids'], list))
        self.assertTrue(isinstance(old_data['uuids'], dict))
        self.assertEqual(old_data['uuids']['uuid1']['order'], u'0')
        self.assertEqual(old_data['uuids']['uuid2']['order'], u'2')
        self.assertEqual(old_data['uuids']['uuid3']['order'], u'1')
