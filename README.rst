*********************************
.gov.br: Blocos de Conteúdo
*********************************

.. contents:: Conteúdo
   :depth: 2

Introdução
----------

Este pacote provê tiles (Blocos de conteúdo) para uso em
sites Plone do Governo da República Federativa do Brasil.

Estado deste pacote
-------------------

O **brasil.gov.tiles** tem testes automatizados e, a cada alteração em seu
código os testes são executados pelo serviço Travis CI.

O estado atual dos testes pode ser visto na imagem a seguir:

.. image:: http://img.shields.io/pypi/v/brasil.gov.tiles.svg
    :target: https://pypi.python.org/pypi/brasil.gov.tiles

.. image:: https://img.shields.io/travis/plonegovbr/brasil.gov.tiles/master.svg
    :target: http://travis-ci.org/plonegovbr/brasil.gov.tiles

.. image:: https://img.shields.io/coveralls/plonegovbr/brasil.gov.tiles/master.svg
    :target: https://coveralls.io/r/plonegovbr/brasil.gov.tiles

Instalação
----------

Para habilitar a instalação deste produto em um ambiente que utilize o
buildout:

1. Editar o arquivo buildout.cfg (ou outro arquivo de configuração) e
   adicionar o pacote ``brasil.gov.tiles`` à lista de eggs da instalação:

.. code-block:: ini

    [buildout]
    ...
    eggs =
        brasil.gov.tiles


2. Após alterar o arquivo de configuração é necessário executar
   ''bin/buildout'', que atualizará sua instalação.

3. Reinicie o Plone

4. Acesse o painel de controle e na opção **tiles** você verá os tiles
providos por este pacote listados.
