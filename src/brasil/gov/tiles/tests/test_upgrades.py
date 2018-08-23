# -*- coding: utf-8 -*-
from brasil.gov.tiles import utils
from brasil.gov.tiles.testing import INTEGRATION_TESTING
from plone import api

import unittest


class BaseUpgradeTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING
    profile_id = u'brasil.gov.tiles:default'

    def setUp(self):
        self.portal = self.layer['portal']
        self.setup = self.portal['portal_setup']
        self.setup.setLastVersionForProfile(self.profile_id, self.from_)

    def _get_upgrade_step_by_title(self, title):
        """Return the upgrade step that matches the title specified."""
        self.setup.setLastVersionForProfile(self.profile_id, self.from_)
        upgrades = self.setup.listUpgrades(self.profile_id)
        steps = [s for s in upgrades[0] if s['title'] == title]
        return steps[0] if steps else None

    def _do_upgrade(self, step):
        """Execute an upgrade step."""
        request = self.layer['request']
        request.form['profile_id'] = self.profile_id
        request.form['upgrades'] = [step['id']]
        self.setup.manage_doUpgrades(request=request)


class UpgradeTo4100TestCase(BaseUpgradeTestCase):

    from_ = u'*'
    to_ = u'4100'

    def test_profile_version(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertEqual(version, self.from_)

    def test_registered_steps(self):
        steps = len(self.setup.listUpgrades(self.profile_id)[0])
        self.assertEqual(steps, 10)

    def test_update_resources_references(self):
        # address also an issue with Setup permission
        title = u'Use resources compiled from webpack'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)

        # simulate state on previous version
        from brasil.gov.tiles.upgrades.v4100 import _rename_resources
        from brasil.gov.tiles.upgrades.v4100 import RESOURCES_TO_UPDATE
        RESOURCES_TO_UPDATE_INVERSE = {v: k for k, v in RESOURCES_TO_UPDATE.items()}

        css_tool = api.portal.get_tool('portal_css')
        _rename_resources(css_tool, RESOURCES_TO_UPDATE_INVERSE)

        js_tool = api.portal.get_tool('portal_javascripts')
        _rename_resources(js_tool, RESOURCES_TO_UPDATE_INVERSE)

        css_ids = css_tool.getResourceIds()
        self.assertIn('++resource++brasil.gov.tiles/tiles.css', css_ids)
        self.assertIn('++resource++brasil.gov.tiles/swiper.min.css', css_ids)
        self.assertNotIn('++resource++brasil.gov.tiles/brasilgovtiles.css', css_ids)
        self.assertNotIn('++resource++brasil.gov.tiles/vendor/swiper.min.css', css_ids)

        js_ids = js_tool.getResourceIds()
        self.assertIn('++resource++brasil.gov.tiles/tiles.js', js_ids)
        self.assertIn('++resource++brasil.gov.tiles/jquery.cycle2.carousel.js', js_ids)
        self.assertIn('++resource++brasil.gov.tiles/jquery.cycle2.js', js_ids)
        self.assertIn('++resource++brasil.gov.tiles/jquery.jplayer.min.js', js_ids)
        self.assertIn('++resource++brasil.gov.tiles/swiper.min.js', js_ids)
        self.assertNotIn('++resource++brasil.gov.tiles/vendor/brasilgovtiles.js', js_ids)
        self.assertNotIn('++resource++brasil.gov.tiles/vendor/jquery.cycle2.carousel.js', js_ids)
        self.assertNotIn('++resource++brasil.gov.tiles/vendor/jquery.cycle2.js', js_ids)
        self.assertNotIn('++resource++brasil.gov.tiles/vendor/jquery.jplayer.min.js', js_ids)
        self.assertNotIn('++resource++brasil.gov.tiles/vendor/swiper.min.js', js_ids)

        # run the upgrade step to validate the update
        self._do_upgrade(step)

        css_ids = css_tool.getResourceIds()
        self.assertIn('++resource++brasil.gov.tiles/brasilgovtiles.css', css_ids)
        self.assertIn('++resource++brasil.gov.tiles/vendor/swiper.min.css', css_ids)
        self.assertNotIn('++resource++brasil.gov.tiles/tiles.css', css_ids)
        self.assertNotIn('++resource++brasil.gov.tiles/swiper.min.css', css_ids)

        js_ids = js_tool.getResourceIds()
        self.assertIn('++resource++brasil.gov.tiles/brasilgovtiles.js', js_ids)
        self.assertIn('++resource++brasil.gov.tiles/vendor/jquery.cycle2.carousel.js', js_ids)
        self.assertIn('++resource++brasil.gov.tiles/vendor/jquery.cycle2.js', js_ids)
        self.assertIn('++resource++brasil.gov.tiles/vendor/jquery.jplayer.min.js', js_ids)
        self.assertIn('++resource++brasil.gov.tiles/vendor/swiper.min.js', js_ids)
        self.assertNotIn('++resource++brasil.gov.tiles/tiles.js', js_ids)
        self.assertNotIn('++resource++brasil.gov.tiles/jquery.cycle2.carousel.js', js_ids)
        self.assertNotIn('++resource++brasil.gov.tiles/jquery.cycle2.js', js_ids)
        self.assertNotIn('++resource++brasil.gov.tiles/jquery.jplayer.min.js', js_ids)
        self.assertNotIn('++resource++brasil.gov.tiles/swiper.min.js', js_ids)

    def test_remove_deprecated_tiles(self):
        title = u'Remove deprecated tiles'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)

        # run the upgrade step to validate the update
        self._do_upgrade(step)

        # no easy way to test tile removal: raises ConstraintNotSatisfied

    def test_add_potd_tile(self):
        title = u'Add POTD tile'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)

        tile = u'brasil.gov.tiles.potd'
        utils.disable_tile(tile)

        # run the upgrade step to validate the update
        self._do_upgrade(step)

        self.assertIn(tile, utils.get_registered_tiles())
        self.assertIn(tile, utils.get_available_tiles())

    def test_add_quote_tile(self):
        title = u'Add Quote tile'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)

        tile = u'brasil.gov.tiles.quote'
        utils.disable_tile(tile)

        # run the upgrade step to validate the update
        self._do_upgrade(step)

        self.assertIn(tile, utils.get_registered_tiles())
        self.assertIn(tile, utils.get_available_tiles())

    def test_add_photogallery_tile(self):
        title = u'Add Photo Gallery tile'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)

        tile = u'brasil.gov.tiles.photogallery'
        utils.disable_tile(tile)

        # run the upgrade step to validate the update
        self._do_upgrade(step)

        self.assertIn(tile, utils.get_registered_tiles())
        self.assertIn(tile, utils.get_available_tiles())

    def test_add_navigation_tile(self):
        title = u'Add Navigation tile'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)

        tile = u'brasil.gov.tiles.navigation'
        utils.disable_tile(tile)

        # run the upgrade step to validate the update
        self._do_upgrade(step)

        self.assertIn(tile, utils.get_registered_tiles())
        self.assertIn(tile, utils.get_available_tiles())

    def test_replace_nitf_tile(self):
        title = u'Replace NITF tile'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)

        tile = u'collective.nitf'
        utils.disable_tile(tile)

        # add object with an old tile on its layout
        with api.env.adopt_roles(['Manager']):
            obj = api.content.create(
                self.portal, 'collective.cover.content', 'foo')
        obj.cover_layout = '[{"type": "row", "children": [{"id": "group1", "type": "group", "column-size": 6, "roles": ["Manager"], "children": [{"tile-type": "collective.cover.basic", "type": "tile", "id": "4ebc5e6678044918b76280ec0204041a"}]}, {"type": "group", "column-size": 6, "roles": ["Manager"], "children": [{"tile-type": "nitf", "type": "tile", "id": "7d68fd4cf0e34073aea99568f1e8eef6"}]}]}]'  # noqa: E501
        obj.reindexObject()

        # run the upgrade step to validate the update
        self._do_upgrade(step)

        self.assertIn(tile, utils.get_registered_tiles())
        self.assertIn(tile, utils.get_available_tiles())

        expected = '[{"type": "row", "children": [{"id": "group1", "type": "group", "column-size": 6, "roles": ["Manager"], "children": [{"tile-type": "collective.cover.basic", "type": "tile", "id": "4ebc5e6678044918b76280ec0204041a"}]}, {"type": "group", "column-size": 6, "roles": ["Manager"], "children": [{"tile-type": "collective.nitf", "type": "tile", "id": "7d68fd4cf0e34073aea99568f1e8eef6"}]}]}]'  # noqa: E501
        import json
        self.assertEqual(json.loads(obj.cover_layout), json.loads(expected))

        # no easy way to test image_description attribute change

    def test_update_tile(self):
        title = u'Update Banner tile'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)

        # run the upgrade step to validate the update
        self._do_upgrade(step)

        # no easy way to test image_description attribute change
