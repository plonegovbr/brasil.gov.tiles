# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup

version = '1.1rc1'
long_description = (
    open('README.rst').read() + '\n' +
    open('CONTRIBUTORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(
    name='brasil.gov.tiles',
    version=version,
    description="Tiles para o Portal Padrão do Governo Federal",
    long_description=long_description,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Multimedia",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='plone tiles brasil gov',
    author='PloneGov.BR',
    author_email='gov@plone.org.br',
    url='https://github.com/plonegovbr/brasil.gov.tiles',
    license='GPLv2',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['brasil', 'brasil.gov'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # Após o commit 007adcde40d2031a15debd5122af8086a1db6fa6, necessito a
        # partir dessa versão pois alterei o caminho dos recursos estáticos no
        # overrides.zcml.
        'collective.cover > 1.0a12',
        'collective.nitf',
        'collective.polls',
        'collective.prettydate',
        'five.grok',
        'plone.app.blocks',
        'plone.app.dexterity [grok, relations]',
        'plone.app.iterate',
        'plone.app.layout',
        # BBB: Adiciona plone.app.referenceablebehavior pois ainda não
        # estamos no Plone 5 e o release 1.1b1 de collective.cover
        # remove essa dependência. Ver
        # https://github.com/collective/collective.cover/commit/798ee6cc62c24cb21dacd92bbba70fdb867b8a4a
        'plone.app.referenceablebehavior',
        'plone.app.registry',
        # BBB: Adiciona plone.app.stagingbehavior pois ainda não
        # estamos no Plone 5 e release 1.1b1 de collective.cover
        # remove essa dependência. Ver
        # https://github.com/collective/collective.cover/commit/651cf0b86b45f9398dabc108a14d5c49f79367bf
        'plone.app.stagingbehavior',
        'plone.app.textfield',
        'plone.app.tiles',
        'plone.app.upgrade',
        'plone.app.uuid',
        'plone.app.vocabularies',
        'plone.dexterity',
        'plone.memoize',
        'plone.namedfile',
        'plone.tiles',
        'plone.uuid',
        'Products.CMFCore',
        'Products.CMFPlone >=4.3',
        'Products.GenericSetup',
        'setuptools',
        'z3c.unconfigure',
        'zope.component',
        'zope.interface',
        'zope.schema',
    ],
    extras_require={
        'test': [
            'collective.cover[test]',
            'mock',
            'five.pt',
            'plone.app.robotframework',
            'plone.app.testing [robot] >=4.2.2',
            'plone.browserlayer',
            'plone.cachepurging',
            'plone.testing',
            'Products.PloneFormGen',
        ]
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
