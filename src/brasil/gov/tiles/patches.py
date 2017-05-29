# -*- coding: utf-8 -*-
from brasil.gov.tiles.config import PROJECTNAME
from collective.cover.tiles.base import PersistentCoverTile
from collective.cover.tiles.list import ListTile
from plone import api
from plone.app.uuid.utils import uuidToObject
from plone.tiles.interfaces import ITileDataManager
from Products.CMFPlone.utils import safe_hasattr

import logging

logger = logging.getLogger(PROJECTNAME)


# FIXME: A partir da versão 1.2b1 de collective.cover, esse método fica idêntico
# ao do cover, portanto podemos remover o patch. Ver
# https://github.com/collective/collective.cover/commit/646f42b8959fdedd274940908b6734431cbd8110
# Lembre de fechar o relato em https://github.com/plonegovbr/brasil.gov.tiles/issues/170
def persistent_cover_tile():
    def _has_image_field(self, obj):
        """Return True if the object has an image field.

        :param obj: [required]
        :type obj: content object
        """
        if safe_hasattr(obj, 'image'):  # Dexterity
            return True
        elif safe_hasattr(obj, 'Schema'):  # Archetypes
            return 'image' in obj.Schema().keys()
        else:
            return False

    setattr(PersistentCoverTile,
            '_has_image_field',
            _has_image_field)
    logger.info('Patched PersistentCoverTile cover class')


def results():
    # FIXME
    # Esse patch, caso o relato abaixo
    # https://github.com/collective/collective.cover/issues/716
    # seja aceito, poderá ser removido.
    # A lógica de usar int em key=lambda x: int(x[1]['order'] não existe no
    # collective 1.1b1 usado atualmente, mas foi adicionado em
    # https://github.com/collective/collective.cover/pull/717/commits/75cba5e056c21c80e9ef1d5190117c0e7a3275fa
    # disponível na versão 1.4b2. Foi desse commit também de onde o código do
    # patch foi copiado para posterior adição da lógica do portal_type.
    def _results_patch(self, portal_type=None):
        """Return the list of objects stored in the tile as UUID. If an UUID
        has no object associated with it, removes the UUID from the list.
        :returns: a list of objects.
        """
        self.set_limit()

        # always get the latest data
        uuids = ITileDataManager(self).get().get('uuids', None)

        results = list()
        if uuids:
            ordered_uuids = [(k, v) for k, v in uuids.items()]
            ordered_uuids.sort(key=lambda x: int(x[1]['order']))

            for uuid in [i[0] for i in ordered_uuids]:
                obj = uuidToObject(uuid)
                if obj:
                    if portal_type is None:
                        results.append(obj)
                    else:
                        if obj.portal_type in portal_type:
                            results.append(obj)
                else:
                    # maybe the user has no permission to access the object
                    # so we try to get it bypassing the restrictions
                    catalog = api.portal.get_tool('portal_catalog')
                    brain = catalog.unrestrictedSearchResults(UID=uuid)
                    if not brain:
                        # the object was deleted; remove it from the tile
                        self.remove_item(uuid)
                        logger.debug(
                            'Nonexistent object {0} removed from '
                            'tile'.format(uuid)
                        )

        return results[:self.limit]

    setattr(ListTile,
            'results',
            _results_patch)
    logger.info('Patched ListTile cover class')


def run():
    persistent_cover_tile()
    results()
