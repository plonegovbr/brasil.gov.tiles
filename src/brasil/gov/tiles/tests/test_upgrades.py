# -*- coding: utf-8 -*-
from brasil.gov.tiles import utils
from brasil.gov.tiles.testing import INTEGRATION_TESTING
from collective.cover.controlpanel import ICoverSettings
from plone import api

import json
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
        self.assertNotIn('++resource++brasil.gov.tiles/brasilgovtiles.css', css_ids)

        js_ids = js_tool.getResourceIds()
        self.assertIn('++resource++brasil.gov.tiles/tiles.js', js_ids)
        self.assertIn('++resource++brasil.gov.tiles/jquery.cycle2.carousel.js', js_ids)
        self.assertIn('++resource++brasil.gov.tiles/jquery.cycle2.js', js_ids)
        self.assertIn('++resource++brasil.gov.tiles/jquery.jplayer.min.js', js_ids)
        self.assertNotIn('++resource++brasil.gov.tiles/vendor/brasilgovtiles.js', js_ids)
        self.assertNotIn('++resource++brasil.gov.tiles/vendor/jquery.cycle2.carousel.js', js_ids)
        self.assertNotIn('++resource++brasil.gov.tiles/vendor/jquery.cycle2.js', js_ids)
        self.assertNotIn('++resource++brasil.gov.tiles/vendor/jquery.jplayer.min.js', js_ids)

        # run the upgrade step to validate the update
        self._do_upgrade(step)

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

    def test_disable_deprecated_tiles(self):
        title = u'Disable deprecated tiles'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)

        # run the upgrade step to validate the update
        self._do_upgrade(step)

        # no easy way to test it as adding them raises ConstraintNotSatisfied

    def test_add_new_tiles(self):
        title = u'Add new tiles'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)

        from brasil.gov.tiles.upgrades.v4100 import NEW_TILES
        for tile in NEW_TILES:
            utils.disable_tile(tile)

        # run the upgrade step to validate the update
        self._do_upgrade(step)

        for tile in NEW_TILES:
            self.assertIn(tile, utils.get_registered_tiles())
            self.assertIn(tile, utils.get_available_tiles())

    def test_migrate_deprecated_tiles(self):
        title = u'Migrate deprecated tiles'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)

        # add object with an old tile on its layout
        from brasil.gov.tiles.upgrades.v4100 import DEPRECATED_TILES
        with api.env.adopt_roles(['Manager']):
            obj = api.content.create(
                self.portal, 'collective.cover.content', 'foo')

        for old, new in DEPRECATED_TILES:
            layout = '[{{"type": "row", "children": [{{"id": "group1", "type": "group", "column-size": 6, "roles": ["Manager"], "children": [{{"tile-type": "collective.cover.basic", "type": "tile", "id": "4ebc5e6678044918b76280ec0204041a"}}]}}, {{"type": "group", "column-size": 6, "roles": ["Manager"], "children": [{{"tile-type": "{0}", "type": "tile", "id": "7d68fd4cf0e34073aea99568f1e8eef6"}}]}}]}}]'  # noqa: E501
            obj.cover_layout = layout.format(old)
            obj.reindexObject()

            # run the upgrade step to validate the update
            self._do_upgrade(step)

            # self.assertEqual(obj.list_tiles(old), [])  # tile not listed
            if new is None:
                # tile must be removed from layout
                layout = '[{{"type": "row", "children": [{{"children": [{{"tile-type": "collective.cover.basic", "type": "tile", "id": "4ebc5e6678044918b76280ec0204041a"}}], "type": "group", "id": "group1", "roles": ["Manager"], "column-size": 6}}, {{"type": "group", "children": [], "roles": ["Manager"], "column-size": 6}}]}}]'  # noqa: E501
            else:
                # tile must be migrated in layout
                layout = '[{{"type": "row", "children": [{{"id": "group1", "type": "group", "column-size": 6, "roles": ["Manager"], "children": [{{"tile-type": "collective.cover.basic", "type": "tile", "id": "4ebc5e6678044918b76280ec0204041a"}}]}}, {{"type": "group", "column-size": 6, "roles": ["Manager"], "children": [{{"tile-type": "{0}", "type": "tile", "id": "7d68fd4cf0e34073aea99568f1e8eef6"}}]}}]}}]'  # noqa: E501

            expected = layout.format(new)
            self.assertEqual(json.loads(obj.cover_layout), json.loads(expected))

            # TODO: no easy way to test image_description attribute change

    def test_install_embedder(self):
        title = u'Install sc.embedder'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)

        # simulate state on previous version
        addon = 'sc.embedder'
        qi = api.portal.get_tool('portal_quickinstaller')
        with api.env.adopt_roles(['Manager']):
            qi.uninstallProducts([addon])
        self.assertFalse(qi.isProductInstalled(addon))

        # execute upgrade step and verify changes were applied
        self._do_upgrade(step)
        self.assertTrue(qi.isProductInstalled(addon))

    @staticmethod
    def get_searchable_content_types():
        """Return a list of searchable content types."""
        record = dict(interface=ICoverSettings, name='searchable_content_types')
        return api.portal.get_registry_record(**record)

    @staticmethod
    def set_searchable_content_types(value):
        """Set a list of searchable content types."""
        record = dict(interface=ICoverSettings, name='searchable_content_types')
        api.portal.set_registry_record(value=value, **record)

    def test_make_embedder_searchable(self):
        title = u'Make Embedder searchable at collective.cover'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)

        content_type = 'sc.embedder'
        searchable_content_types = self.get_searchable_content_types()
        searchable_content_types.remove(content_type)
        self.set_searchable_content_types(searchable_content_types)
        self.assertNotIn(content_type, self.get_searchable_content_types())

        # run the upgrade step to validate the update
        self._do_upgrade(step)

        self.assertIn(content_type, self.get_searchable_content_types())

    def test_avoid_searchable_content_types_duplication(self):
        title = u'Avoid searchable_content_types duplication'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)

        # simulate state on previous version
        from collections import Counter
        record = dict(interface=ICoverSettings, name='searchable_content_types')  # noqa: E501
        content_types = api.portal.get_registry_record(**record)
        content_types += ['Document', 'Document', 'News Item']
        api.portal.set_registry_record(value=content_types, **record)
        content_types = api.portal.get_registry_record(**record)
        self.assertEqual(max(Counter(content_types).values()), 3)

        # run the upgrade step to validate the update
        self._do_upgrade(step)
        content_types = api.portal.get_registry_record(**record)
        self.assertEqual(max(Counter(content_types).values()), 1)
