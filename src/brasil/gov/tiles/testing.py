# -*- coding: utf-8 -*-
from App.Common import package_home
from collective.cover.testing import Fixture as CoverFixture
from PIL import Image
from plone import api
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.namedfile.file import NamedBlobFile
from plone.namedfile.file import NamedImage
from plone.testing import z2
from sc.embedder.tests.test_content import PROVIDERS
from StringIO import StringIO

import os
import random
import unittest


VIDEO_PREFIX = 'youtube'
TOTAL_VIDEOS = 4


def loadFile(name, size=0):
    """Load file from testing directory
    """
    path = os.path.join(package_home(globals()), 'tests/files', name)
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

    output = StringIO()
    image.save(output, format='PNG')
    return output.getvalue()


class Fixture(CoverFixture):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        super(Fixture, self).setUpZope(app, configurationContext)
        import brasil.gov.tiles
        import sc.embedder
        self.loadZCML(package=brasil.gov.tiles)
        self.loadZCML(package=sc.embedder)
        self.loadZCML(name='overrides.zcml', package=brasil.gov.tiles)

    def setUpPloneSite(self, portal):
        super(Fixture, self).setUpPloneSite(portal)
        with api.env.adopt_roles(roles=['Manager']):

            # Install into Plone site using portal_setup
            self.applyProfile(portal, 'brasil.gov.tiles:default')
            self.applyProfile(portal, 'brasil.gov.tiles:testfixture')
            self.applyProfile(portal, 'sc.embedder:default')

            # NITF
            api.content.create(
                type='Folder',
                title='my-news-folder',
                container=portal
            )
            api.content.create(
                type='collective.nitf.content',
                title='my-nitf-without-image',
                container=portal['my-news-folder']
            )
            api.content.create(
                type='collective.nitf.content',
                title='my-nitf-with-image',
                container=portal['my-news-folder']
            )
            api.content.create(
                type='Image',
                title='my-image',
                container=portal['my-news-folder']['my-nitf-with-image']
            ).setImage(generate_jpeg(50, 50))
            portal['my-news-folder'].reindexObject()
            portal['my-news-folder']['my-nitf-with-image'].reindexObject()
            portal['my-news-folder']['my-nitf-without-image'].reindexObject()
            portal['my-news-folder']['my-nitf-with-image']['my-image'].reindexObject()
            #

            # AUDIO
            # Esse arquivo veio de brasil.gov.portal.
            mp3_blob = NamedBlobFile(
                loadFile('file.mp3'),
                'audio/mp3',
                u'file.mp3'
            )

            api.content.create(
                type='Folder',
                title='my-audios',
                container=portal
            )
            portal['my-audios'].reindexObject()

            mp3_obj = api.content.create(
                type='File',
                container=portal['my-audios'],
                id='my-audio'
            )
            mp3_obj.file = mp3_blob
            portal['my-audios']['my-audio'].reindexObject()

            mp3_obj1 = api.content.create(
                type='File',
                container=portal['my-audios'],
                id='my-audio1'
            )
            mp3_obj1.file = mp3_blob
            portal['my-audios']['my-audio1'].reindexObject()

            mp3_obj2 = api.content.create(
                type='File',
                container=portal['my-audios'],
                id='my-audio2'
            )
            mp3_obj2.file = mp3_blob
            portal['my-audios']['my-audio2'].reindexObject()
            #

            # VIDEO
            api.content.create(
                type='Folder',
                title='my-videos',
                container=portal
            )
            portal['my-videos'].reindexObject()
            width = 459
            height = 344
            iframe = '<iframe allowfullscreen="" height="{0}" src="{1}" width="{2}"></iframe>'
            for i in range(0, TOTAL_VIDEOS):
                obj = api.content.create(
                    type='sc.embedder',
                    title='{0}_{1}'.format(VIDEO_PREFIX, str(i)),
                    container=portal['my-videos'],
                    url=PROVIDERS['youtube'],
                    width=width,
                    height=height,
                    embed_html=iframe.format(height, PROVIDERS['youtube'], width),
                    image=NamedImage(generate_jpeg(459, 344))
                )
                obj.reindexObject()
            #


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
