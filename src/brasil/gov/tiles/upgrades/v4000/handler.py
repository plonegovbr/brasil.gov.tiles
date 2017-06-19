# -*- coding: utf-8 -*-
from brasil.gov.tiles.config import PROJECTNAME
from collective.cover.upgrades import upgrade_carousel_tiles_custom_url

import logging


def fix_persistentmap_to_dict_destaque(context):
    """
    O tile do tipo "Destaque" herda do tipo "Lista" de collective.cover.

    No momento que esse tile foi criado, herdando do tipo lista, os métodos que
    "populam" a capa com os uuids também foram copiados. Isso pode ser visto em

        https://raw.githubusercontent.com/plonegovbr/brasil.gov.tiles/1.0a1/src/brasil/gov/tiles/tiles/destaque.py
        https://raw.githubusercontent.com/collective/collective.cover/1.0a2/src/collective/cover/tiles/list.py

    Com a atualização do collective.cover, esses métodos, no tipo "Lista" em
    collective.cover, foram alterados e um upgrade step fornecido em

        https://github.com/collective/collective.cover/blob/master/src/collective/cover/upgrades/v11/__init__.py

    para alterar a forma como estavam armazenados.

    Como o collective.cover evoluiu mas a sobrescrita desses métodos do tipo
    lista não foi removida do tile "Destaque" bem brasil.gov.tiles também nesse
    interim, a forma de armazenamento continua sendo "List", e
    precisa ser corrigido para que possamos atualizar a versão do
    collective.cover.

    Portanto, após a remoção dos métodos do tile "Destaque" por herdar do tipo
    "Lista", preciso chamar NOVAMENTE o upgradeStep do collective.cover, mas
    não ele todo, apenas o método que faz essa correção.

    Mais informações sobre essa migração podem ser vistas em

        https://github.com/plonegovbr/brasil.gov.tiles/issues/130#issuecomment-117761638

    """
    logger = logging.getLogger(PROJECTNAME)
    upgrade_carousel_tiles_custom_url(context)
    logger.info('Applied upgrade profile to version 4000')
