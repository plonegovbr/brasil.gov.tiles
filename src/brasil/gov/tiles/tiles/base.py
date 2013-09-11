# -*- coding: utf-8 -*-

from collective.cover.tiles.base import IPersistentCoverTile
from collective.cover.tiles.base import PersistentCoverTile as PersistentCoverTileOriginal

class PersistentCoverTile(PersistentCoverTileOriginal):
    """Customization to add a method to check if there is image into object
       TODO: This should be took out when collective.cover 1.0a5 be released
             because the original class will have the same method.
    """

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
