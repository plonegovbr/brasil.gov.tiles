# -*- coding: utf-8 -*-
"""
Preciso de um arquivo separado para esse patch.

Isso ocorre porque se eu coloco para importar

    from brasil.gov.tiles.tiles.list import IListTile as brasilIListTile

em patches.py, dá erro de dependência circular porque brasilIListTile importa
o message factory padrão de brasil.gov.tiles, mas ele é definido no __init__.py
do pacote que chama a importação dando o erro de import:

  File "brasil/gov/tiles/__init__.py", line 2, in <module>
    from brasil.gov.tiles import patches
  File "brasil/gov/tiles/patches.py", line 3, in <module>
    from brasil.gov.tiles.tiles.list import IListTile
  File "brasil/gov/tiles/tiles/list.py", line 2, in <module>
    from brasil.gov.tiles import _ as _
zope.configuration.xmlconfig.ZopeXMLConfigurationError: File "parts/instance/etc/site.zcml", line 12.2-12.39
    ZopeXMLConfigurationError: File "Products/CMFPlone/meta.zcml", line 42.4-46.10
    ImportError: cannot import name _

Como esse patch é temporário, na hora da remoção esse arquivo pode ser removido
por completo.

"""

from brasil.gov.tiles.tiles.list import IListTile as brasilIListTile
from collective.cover.tiles.list import IListTile
from zExceptions import BadRequest


def render_banner_rotativo(self):
    """
    Customizado de

    https://github.com/collective/collective.cover/blob/1.1b1/src/collective/cover/browser/cover.py#L327
    """
    tile_type = self.request.form.get('tile-type')
    tile_id = self.request.form.get('tile-id')
    uuid = self.request.form.get('uuid')
    if tile_type and tile_id and uuid:
        tile = self.context.restrictedTraverse('{0}/{1}'.format(tile_type, tile_id))
        # Essa chamada foi a única customização do método.
        if IListTile.providedBy(tile) or brasilIListTile.providedBy(tile):
            tile.remove_item(uuid)
            # reinstantiate the tile to update its content on AJAX calls
            tile = self.context.restrictedTraverse('{0}/{1}'.format(tile_type, tile_id))
            return tile()
    else:
        raise BadRequest('Invalid parameters')


def render(self):
    """Preocupe-se apenas com o banner_rotativo."""
    tile_type = self.request.form.get('tile-type')
    if tile_type == 'banner_rotativo':
        render_banner_rotativo(self)
    else:
        self._old_render()
