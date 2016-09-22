# -*- coding: utf-8 -*-
from brasil.gov.tiles.testing import INTEGRATION_TESTING
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


class Upgrade4000to4001TestCase(UpgradeTestCaseBrasilGovTitles):

    layer = INTEGRATION_TESTING

    def setUp(self):
        super(Upgrade4000to4001TestCase, self).setUp(u'4000', u'4001')

    def test_upgrades_cover(self):
        title = u'Upgrades carrossel cover'
        step = self._get_upgrade_step(title)
        self.assertIsNotNone(step)

        # simulate state on previous version
        cover = self._create_cover('test-cover', 'Empty layout')

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
