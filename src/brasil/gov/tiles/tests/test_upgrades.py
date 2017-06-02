# -*- coding: utf-8 -*-
from brasil.gov.tiles.testing import INTEGRATION_TESTING
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


class Upgrade4001to4002TestCase(UpgradeTestCaseBrasilGovTitles):

    layer = INTEGRATION_TESTING

    def setUp(self):
        super(Upgrade4001to4002TestCase, self).setUp(u'4001', u'4002')

    def _upgrade_carousel_tiles_custom_url(self, tiles_uuids, cover_data):
        title = u'Upgrades lista cover'
        step = self._get_upgrade_step(title)
        self.assertIsNotNone(step)

        cover = self._create_cover('test-cover-upgrades-lista', 'Empty layout')
        cover.cover_layout = cover_data
        for i in tiles_uuids:
            tile = cover.get_tile(i)
            data = ITileDataManager(tile).get()
            data['uuids'] = ['uuid1', 'uuid3', 'uuid2']
            ITileDataManager(tile).set(data)

        self._do_upgrade_step(step)

        for i in tiles_uuids:
            tile = cover.get_tile(i)
            new_data = ITileDataManager(tile).get()
            self.assertFalse(isinstance(new_data['uuids'], list))
            self.assertTrue(isinstance(new_data['uuids'], dict))
            self.assertEqual(new_data['uuids']['uuid1']['order'], u'0')
            self.assertEqual(new_data['uuids']['uuid2']['order'], u'2')
            self.assertEqual(new_data['uuids']['uuid3']['order'], u'1')

    def _corrige_uuids_se_colecao_ou_folder_e_seta_footer_text(self, tiles_uuids, cover_data):
        title = u'Corrige referência de coleção e diretório e seus filhos em audiogallery, videogallery e mediacarousel.'
        step = self._get_upgrade_step(title)
        self.assertIsNotNone(step)

        # Para facilitar os testes e o for, iremos utilizar apenas um diretório
        # para três tipos de tiles diferentes: a função aqui é verificar uuids
        # e não é necessária renderização da interface pra isso, portanto usar
        # um só diretório não terá problema.

        # Se não for 'str', é um método por ser ATFolder ao invés de apenas
        # Folder.
        uid_container = self.portal['my-audios'].UID
        if type(uid_container) not in [str, unicode]:
            uid_container = uid_container()

        cover = self._create_cover('test-cover-colecao-diretorio', 'Empty layout')
        cover.cover_layout = cover_data
        old_uuids = []
        for i in tiles_uuids:
            old_uuids_tile = [j.UID for j in self.portal['my-audios'].getFolderContents()]
            tile = cover.get_tile(i)
            data = ITileDataManager(tile).get()
            data['uuids'] = [uid_container]
            ITileDataManager(tile).set(data)
            old_uuids.append(old_uuids_tile)

        self._do_upgrade_step(step)

        for i, j in enumerate(tiles_uuids):
            tile = cover.get_tile(j)
            new_data = ITileDataManager(tile).get()
            self.assertTrue(new_data.get('footer_text', None) is not None)
            self.assertEqual(
                new_data.get('footer_text', None),
                self.portal['my-audios'].absolute_url()
            )
            self.assertEqual(
                sorted(new_data['uuids'], key=new_data['uuids'].__getitem__),
                old_uuids[i]
            )
            self.assertFalse(isinstance(new_data['uuids'], list))
            self.assertTrue(isinstance(new_data['uuids'], dict))
            if tile.__name__ == 'videogallery':
                self.assertTrue(new_data.get('uuid_container', None) is not None)
                self.assertEqual(
                    new_data.get('uuid_container'),
                    uid_container
                )

    def _upgrades_tile_header_tile_title(self, tiles_uuids, cover_data):
        title = u'Upgrade atributo header para tile_title'
        step = self._get_upgrade_step(title)
        self.assertIsNotNone(step)
        cover = self._create_cover('test-cover-header', 'Empty layout')
        cover.cover_layout = cover_data
        for i in tiles_uuids:
            tile = cover.get_tile(i)
            data = ITileDataManager(tile).get()
            data['header'] = 'header'
            ITileDataManager(tile).set(data)

        self._do_upgrade_step(step)

        for i in tiles_uuids:
            tile = cover.get_tile(i)
            new_data = ITileDataManager(tile).get()
            self.assertTrue(new_data.get('header', None) is None)
            self.assertTrue(new_data.get('tile_title', None) is not None)

    def test_upgrade_to_4002(self):
        # Isso poderia ser mais dinâmico, por exemplo, pegando a variável
        # TILE_TYPES, dando um for e etc. O problema é que além de ficar mais
        # complexo, teria de adicionar escape em '{' e '}' o tempo todo devido
        # ao uso de string.format.

        # Esses uuids são "arbitrários",  mas serão adicionados "na mão" em
        # cover_data na mesma ordem que estão nessa lista.
        tiles_uuids = ['ca6ba6675ef145e4a569c5e410af751',
                       'ca6ba6675ef145e4a569c5e410af752',
                       'ca6ba6675ef145e4a569c5e410af753']
        cover_data = """[{"type": "row", "children": [{"data": {"layout-type": "column", "column-size": 16}, "type": "group", "children": [{"tile-type": "audiogallery", "type": "tile", "id": "ca6ba6675ef145e4a569c5e410af751"}, {"tile-type": "videogallery", "type": "tile", "id": "ca6ba6675ef145e4a569c5e410af752"}, {"tile-type": "mediacarousel", "type": "tile", "id": "ca6ba6675ef145e4a569c5e410af753"}], "roles": ["Manager"]}]}]"""

        self._upgrade_carousel_tiles_custom_url(tiles_uuids, cover_data)

        self._upgrades_tile_header_tile_title(tiles_uuids, cover_data)

        self._corrige_uuids_se_colecao_ou_folder_e_seta_footer_text(
            tiles_uuids,
            cover_data
        )
