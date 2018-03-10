# -*- coding: utf-8 -*-
from brasil.gov.tiles.testing import INTEGRATION_TESTING
from collective.cover.config import IS_PLONE_5
from collective.cover.tests.test_upgrades import UpgradeTestCaseBase
from plone import api

import unittest


class UpgradeTestCaseBrasilGovTitles(UpgradeTestCaseBase):
    """
    Classe que altera o profile_id para 'brasil.gov.tiles:default'
    """

    def setUp(self, from_version, to_version):
        UpgradeTestCaseBase.setUp(self, from_version, to_version)
        self.profile_id = u'brasil.gov.tiles:default'


class Upgrade4004to4005TestCase(UpgradeTestCaseBrasilGovTitles):

    layer = INTEGRATION_TESTING

    def setUp(self):
        super(Upgrade4004to4005TestCase, self).setUp(u'4004', u'4005')

    def test_registrations(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertTrue(int(version) >= int(self.to_version))
        self.assertEqual(self._how_many_upgrades_to_do(), 3)

    @unittest.skipIf(IS_PLONE_5, 'Upgrade step not supported under Plone 5')
    def test_update_resources_references(self):
        # address also an issue with Setup permission
        title = u'Use resource compiled from webpack'
        step = self._get_upgrade_step(title)
        self.assertIsNotNone(step)

        # simulate state on previous version
        from brasil.gov.tiles.upgrades.v4005 import _rename_resources
        from brasil.gov.tiles.upgrades.v4005 import RESOURCES_TO_UPDATE
        RESOURCES_TO_UPDATE_INVERSE = {v: k for k, v in RESOURCES_TO_UPDATE.items()}

        css_tool = api.portal.get_tool('portal_css')
        _rename_resources(css_tool, RESOURCES_TO_UPDATE_INVERSE)

        js_tool = api.portal.get_tool('portal_javascripts')
        _rename_resources(js_tool, RESOURCES_TO_UPDATE_INVERSE)

        css_ids = css_tool.getResourceIds()
        self.assertIn('++resource++brasil.gov.tiles/tiles.css', css_ids)
        self.assertNotIn('++resource++brasil.gov.tiles/brasilgovtiles.css', css_ids)

        js_ids = js_tool.getResourceIds()
        self.assertIn('++resource++brasil.gov.tiles/tiles.js', js_ids)
        self.assertIn('++resource++brasil.gov.tiles/jquery.cycle2.carousel.js', js_ids)
        self.assertIn('++resource++brasil.gov.tiles/jquery.cycle2.js', js_ids)
        self.assertIn('++resource++brasil.gov.tiles/jquery.jplayer.min.js', js_ids)
        self.assertNotIn('++resource++brasil.gov.tiles/brasilgovtiles.js', js_ids)
        self.assertNotIn('++resource++brasil.gov.tiles/vendor/jquery.cycle2.carousel.js', js_ids)
        self.assertNotIn('++resource++brasil.gov.tiles/vendor/jquery.cycle2.js', js_ids)
        self.assertNotIn('++resource++brasil.gov.tiles/vendor/jquery.jplayer.min.js', js_ids)

        # run the upgrade step to validate the update
        self._do_upgrade_step(step)

        css_ids = css_tool.getResourceIds()
        self.assertIn('++resource++brasil.gov.tiles/brasilgovtiles.css', css_ids)
        self.assertNotIn('++resource++brasil.gov.tiles/tiles.css', css_ids)

        js_ids = js_tool.getResourceIds()
        self.assertIn('++resource++brasil.gov.tiles/brasilgovtiles.js', js_ids)
        self.assertIn('++resource++brasil.gov.tiles/vendor/jquery.cycle2.carousel.js', js_ids)
        self.assertIn('++resource++brasil.gov.tiles/vendor/jquery.cycle2.js', js_ids)
        self.assertIn('++resource++brasil.gov.tiles/vendor/jquery.jplayer.min.js', js_ids)
        self.assertNotIn('++resource++brasil.gov.tiles/tiles.js', js_ids)
        self.assertNotIn('++resource++brasil.gov.tiles/jquery.cycle2.carousel.js', js_ids)
        self.assertNotIn('++resource++brasil.gov.tiles/jquery.cycle2.js', js_ids)
        self.assertNotIn('++resource++brasil.gov.tiles/jquery.jplayer.min.js', js_ids)
