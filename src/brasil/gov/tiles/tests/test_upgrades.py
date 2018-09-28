# -*- coding: utf-8 -*-
from brasil.gov.tiles.testing import INTEGRATION_TESTING
from brasil.gov.tiles.upgrades.v4004 import NEW_TILE
from brasil.gov.tiles.upgrades.v4004 import OLD_TILE
from collective.cover.controlpanel import ICoverSettings
from collective.cover.tests.test_upgrades import Upgrade9to10TestCase
from collective.cover.tests.test_upgrades import UpgradeTestCaseBase
from plone import api
from plone.tiles.interfaces import ITileDataManager


class UpgradeTestCaseBrasilGovTitles(UpgradeTestCaseBase):
    """
    Classe que altera o profile_id para 'brasil.gov.tiles:default'
    """

    def setUp(self, from_version, to_version):
        UpgradeTestCaseBase.setUp(self, from_version, to_version)
        self.profile_id = u'brasil.gov.tiles:default'


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
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertTrue(int(version) >= int(self.to_version))
        self.assertEqual(self._how_many_upgrades_to_do(), 2)

    def test_upgrade_to_4000_registrations(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertTrue(int(version) >= int(self.to_version))
        self.assertEqual(self._how_many_upgrades_to_do(), 2)

    def test_new_uuids_structure(self):
        title = u'Atualiza estrutura no banco do tipo Destaque'
        step = self._get_upgrade_step(title)
        self.assertIsNotNone(step)

        # simulate state on previous version
        cover = self._create_cover(id='test-cover', layout='Empty layout')
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


class Upgrade4000to4001TestCase(UpgradeTestCaseBrasilGovTitles):

    layer = INTEGRATION_TESTING

    def setUp(self):
        super(Upgrade4000to4001TestCase, self).setUp(u'4000', u'4001')

    def test_upgrades_cover(self):
        title = u'Upgrades carrossel cover'
        step = self._get_upgrade_step(title)
        self.assertIsNotNone(step)

        # simulate state on previous version
        cover = self._create_cover(id='test-cover', layout='Empty layout')

        old_data = (
            u'[{"type": "row", "children": [{"data": {"layout-type": '
            u'"column", "column-size": 16}, "type": "group", "children": '
            u'[{"tile-type": "collective.cover.carousel", "type": "tile", '
            u'"id": "ca6ba6675ef145e4a569c5e410af7511"}], "roles": '
            u'["Manager"]}]}]'
        )

        expected = (
            u'[{"type": "row", "children": [{"type": "group", "children": '
            u'[{"tile-type": "collective.cover.carousel", "type": "tile", '
            u'"id": "ca6ba6675ef145e4a569c5e410af7511"}], "roles": '
            u'["Manager"], "column-size": 16}]}]'
        )

        cover.cover_layout = old_data
        tile = cover.get_tile('ca6ba6675ef145e4a569c5e410af7511')
        data = ITileDataManager(tile).get()
        data['uuids'] = ['uuid1', 'uuid3', 'uuid2']
        ITileDataManager(tile).set(data)

        # simulate state on previous version of registry layouts
        record = 'collective.cover.controlpanel.ICoverSettings.layouts'
        api.portal.set_registry_record(record, {u'test_layout': old_data})

        # run the upgrade step to validate the update
        self._do_upgrade_step(step)

        # validate upgrade_carousel_tiles_custom_url
        new_data = ITileDataManager(tile).get()
        self.assertFalse(isinstance(new_data['uuids'], list))
        self.assertTrue(isinstance(new_data['uuids'], dict))
        self.assertEqual(new_data['uuids']['uuid1']['order'], u'0')
        self.assertEqual(new_data['uuids']['uuid2']['order'], u'2')
        self.assertEqual(new_data['uuids']['uuid3']['order'], u'1')

        # validate simplify_layout
        self.assertEqual(api.portal.get_registry_record(record),
                         {u'test_layout': expected})
        self.assertEqual(cover.cover_layout, expected)


class Upgrade4001to4002TestCase(UpgradeTestCaseBrasilGovTitles):

    layer = INTEGRATION_TESTING

    def setUp(self):
        super(Upgrade4001to4002TestCase, self).setUp(u'4001', u'4002')

    def test_remove_collective_nitf_tile(self):
        title = u'Remove tile collective.nitf'
        step = self._get_upgrade_step(title)
        self.assertIsNotNone(step)

        # Simula a situação de ter isso registrado porque removemos esse tile
        # no post_handler.
        tiles = api.portal.get_registry_record('plone.app.tiles')
        tiles.append(u'collective.nitf')
        api.portal.set_registry_record('plone.app.tiles', tiles)

        tiles = api.portal.get_registry_record('plone.app.tiles')
        self.assertIn(u'collective.nitf', tiles)

        self._do_upgrade_step(step)

        tiles = api.portal.get_registry_record('plone.app.tiles')
        self.assertNotIn(u'collective.nitf', tiles)


class Upgrade4003to4004TestCase(UpgradeTestCaseBrasilGovTitles):

    layer = INTEGRATION_TESTING

    def setUp(self):
        super(Upgrade4003to4004TestCase, self).setUp(u'4003', u'4004')

    def test_replace_poll_tile(self):
        title = u'Replace poll tile'
        step = self._get_upgrade_step(title)
        self.assertIsNotNone(step)

        # Simula a situação de ter isso registrado porque removemos esse tile
        # no post_handler.
        tiles = api.portal.get_registry_record('plone.app.tiles')
        tiles.append(OLD_TILE)
        tiles.remove(NEW_TILE)

        record = dict(interface=ICoverSettings, name='available_tiles')
        available_tiles = api.portal.get_registry_record(**record)
        available_tiles.append(OLD_TILE)
        available_tiles.remove(NEW_TILE)

        tiles = api.portal.get_registry_record('plone.app.tiles')
        self.assertIn(OLD_TILE, tiles)
        self.assertNotIn(NEW_TILE, tiles)

        record = dict(interface=ICoverSettings, name='available_tiles')
        available_tiles = api.portal.get_registry_record(**record)
        self.assertIn(OLD_TILE, available_tiles)
        self.assertNotIn(NEW_TILE, available_tiles)

        # Isso é o que é feito no upgrade v3 de collective.polls. Estamos
        # rodando aqui para simular o erro em
        # https://github.com/plonegovbr/brasil.gov.tiles/issues/212
        # Ou seja, se rodar o upgradeStep de collective.polls antes desse,
        # não pode duplicar o tile.
        profile = 'profile-collective.polls:default'
        setup_tool = api.portal.get_tool('portal_setup')
        setup_tool.runImportStepFromProfile(profile, 'plone.app.registry')
        tiles = api.portal.get_registry_record('plone.app.tiles')
        self.assertIn(NEW_TILE, tiles)

        self._do_upgrade_step(step)

        tiles = api.portal.get_registry_record('plone.app.tiles')
        self.assertNotIn(OLD_TILE, tiles)
        self.assertIn(NEW_TILE, tiles)

        # https://github.com/plonegovbr/brasil.gov.tiles/issues/212
        self.assertEqual(len(tiles), len(set(tiles)))

        record = dict(interface=ICoverSettings, name='available_tiles')
        available_tiles = api.portal.get_registry_record(**record)
        self.assertNotIn(OLD_TILE, available_tiles)
        self.assertIn(NEW_TILE, available_tiles)

        # https://github.com/plonegovbr/brasil.gov.tiles/issues/212
        self.assertEqual(len(available_tiles), len(set(available_tiles)))


class Upgrade4004to4005TestCase(UpgradeTestCaseBrasilGovTitles):

    layer = INTEGRATION_TESTING

    def setUp(self):
        super(Upgrade4004to4005TestCase, self).setUp(u'4004', u'4005')

    def test_duplicated_collective_polls(self):
        title = u'collective.polls duplicado'
        step = self._get_upgrade_step(title)
        self.assertIsNotNone(step)

        # Simula a situação ter collective.polls duplicado.
        tiles = api.portal.get_registry_record('plone.app.tiles')
        self.assertEqual(len(tiles), len(set(tiles)))
        tiles.append(NEW_TILE)
        api.portal.set_registry_record('plone.app.tiles', tiles)
        self.assertNotEqual(len(tiles), len(set(tiles)))

        self._do_upgrade_step(step)

        tiles = api.portal.get_registry_record('plone.app.tiles')
        self.assertEqual(len(tiles), len(set(tiles)))
