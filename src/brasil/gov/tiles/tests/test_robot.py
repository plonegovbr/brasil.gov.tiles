# -*- coding: utf-8 -*-

from brasil.gov.tiles.testing import ROBOT_TESTING
from plone.testing import layered

import os
import robotsuite
import unittest


dirname = os.path.dirname(__file__)
files = os.listdir(dirname)
tests = [f for f in files if f.startswith('test_') and f.endswith('.robot')]

noncritical = ['Expected Failure']


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(
            robotsuite.RobotTestSuite(t, noncritical=noncritical),
            layer=ROBOT_TESTING)
        for t in tests
    ])
    return suite
