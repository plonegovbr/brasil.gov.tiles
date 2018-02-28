# -*- coding: utf-8 -*-
from collective.cover.tests.test_upgrades import UpgradeTestCaseBase


class UpgradeTestCaseBrasilGovTitles(UpgradeTestCaseBase):
    """
    Classe que altera o profile_id para 'brasil.gov.tiles:default'
    """

    def setUp(self, from_version, to_version):
        UpgradeTestCaseBase.setUp(self, from_version, to_version)
        self.profile_id = u'brasil.gov.tiles:default'
