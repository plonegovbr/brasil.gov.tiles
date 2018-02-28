# -*- coding: utf-8 -*-
from __future__ import division  # isort:skip
from future.builtins import range  # isort:skip
from App.Common import package_home
from collective.cover.testing import Fixture as CoverFixture
from io import BytesIO
from PIL import Image
from plone import api
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.testing import z2

import os
import random
import unittest


def loadFile(name, size=0):
    """Load file from testing directory
    """
    path = os.path.join(package_home(globals()), 'tests/input', name)
    fd = open(path, 'rb')
    data = fd.read()
    fd.close()
    return data


def generate_jpeg(width, height):
    # Mandelbrot fractal
    # FB - 201003254
    # drawing area
    xa = -2.0
    xb = 1.0
    ya = -1.5
    yb = 1.5
    maxIt = 25  # max iterations allowed
    # image size
    image = Image.new('RGB', (width, height))
    c = complex(random.random() * 2.0 - 1.0, random.random() - 0.5)

    for y in range(height):
        zy = y * (yb - ya) / (height - 1) + ya
        for x in range(width):
            zx = x * (xb - xa) / (width - 1) + xa
            z = complex(zx, zy)
            for i in range(maxIt):
                if abs(z) > 2.0:
                    break
                z = z * z + c
            r = i % 4 * 64
            g = i % 8 * 32
            b = i % 16 * 16
            image.putpixel((x, y), b * 65536 + g * 256 + r)

    output = BytesIO()
    image.save(output, format='PNG')
    return output.getvalue()


class Fixture(CoverFixture):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        super(Fixture, self).setUpZope(app, configurationContext)
        import brasil.gov.tiles
        self.loadZCML(package=brasil.gov.tiles)
        self.loadZCML(name='overrides.zcml', package=brasil.gov.tiles)

    def setUpPloneSite(self, portal):
        super(Fixture, self).setUpPloneSite(portal)
        with api.env.adopt_roles(roles=['Manager']):

            # Install into Plone site using portal_setup
            self.applyProfile(portal, 'brasil.gov.tiles:default')
            self.applyProfile(portal, 'brasil.gov.tiles:testfixture')

            api.content.create(
                type='Folder',
                title='my-news-folder',
                container=portal,
            )
            api.content.create(
                type='collective.nitf.content',
                title='my-nitf-without-image',
                container=portal['my-news-folder'],
            )
            api.content.create(
                type='collective.nitf.content',
                title='my-nitf-with-image',
                container=portal['my-news-folder'],
            )
            api.content.create(
                type='Image',
                title='my-image',
                container=portal['my-news-folder']['my-nitf-with-image'],
            ).setImage(generate_jpeg(50, 50))
            portal['my-news-folder'].reindexObject()
            portal['my-news-folder']['my-nitf-with-image'].reindexObject()
            portal['my-news-folder']['my-nitf-without-image'].reindexObject()
            portal['my-news-folder']['my-nitf-with-image']['my-image'].reindexObject()


FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='brasil.gov.tiles:Integration',
)
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='brasil.gov.tiles:Functional',
)

ROBOT_TESTING = FunctionalTesting(
    bases=(FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
    name='brasil.gov.tiles:Robot',
)


class BaseIntegrationTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
