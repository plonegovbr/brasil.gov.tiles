# -*- coding:utf-8 -*-
from brasil.gov.tiles.config import PROJECTNAME
from collective.cover.tiles.base import PersistentCoverTile

import logging

logger = logging.getLogger(PROJECTNAME)


def persistent_cover_tile():
    def _has_image_field(self, obj):
        """Return True if the object has an image field.

        :param obj: [required]
        :type obj: content object
        """
        if hasattr(obj, 'image'):  # Dexterity
            return True
        elif hasattr(obj, 'Schema'):  # Archetypes
            return 'image' in obj.Schema().keys()
        else:
            return False

    setattr(PersistentCoverTile,
            '_has_image_field',
            _has_image_field)
    logger.info('Patched PersistentCoverTile cover class')


def run():
    persistent_cover_tile()
