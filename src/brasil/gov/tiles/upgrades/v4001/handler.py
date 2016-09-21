# -*- coding: utf-8 -*-
from brasil.gov.tiles.config import PROJECTNAME
from collective.cover.upgrades import upgrade_carousel_tiles_custom_url
from collective.cover.upgrades.v11 import simplify_layout

import logging


def upgrades_carosel_cover(setup):
    """
    Executa upgrades do cover que não foram executadas na tile de carrossel.

    Como agora estamos utilizando o corrossel do cover, precisamos executar os
    upgrades do carrossel do cover que não foram executados quando existia o
    carrossel no brasil.gov.portal.
    """

    # Esse upgrade não era executado na antiga tile de carrossel do
    # brasil.gov.tiles porque ela não era uma tile de lista e este upgrade era
    # exetutado somente em tiles de lista.
    upgrade_carousel_tiles_custom_url(setup)

    # Garante que o layout dos covers sejam corrigidos. Isso é necessário caso
    # algum cover não tenha sido atualizado quando o upgrade do cover foi
    # executado, deixando o index object_provides sem ser atualizado no
    # catálogo. simplify_layout depende que o index object_provides esteja
    # atualizado. A execução de upgrade_carousel_tiles_custom_url acima,
    # atualiza o cover.
    simplify_layout(setup)

    logger = logging.getLogger(PROJECTNAME)
    logger.info('Executado upgrades do carrossel do cover.')
