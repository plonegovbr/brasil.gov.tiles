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

.. image:: https://img.shields.io/codacy/grade/5a403e23e61d49d195fcb640d1566a89.svg
    :target: https://www.codacy.com/project/plonegovbr/brasil.gov.tiles/dashboard

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

Rodando o buildout de uma tag antiga do pacote
----------------------------------------------

Para atender ao relato de ter vários jobs de integração contínua em pacotes brasil.gov.* (ver https://github.com/plonegovbr/portalpadrao.release/issues/11), no fim da seção extends do buildout.cfg de todos os pacotes brasil.gov.* temos a seguinte linha:

.. code-block:: cfg

    https://raw.githubusercontent.com/plonegovbr/portal.buildout/master/buildout.d/versions.cfg

Hoje, esse arquivo contém sempre as versões pinadas de um release a ser lançado. Por esse motivo, quando é feito o checkout de uma tag mais antiga provavelmente você não conseguirá rodar o buildout. Dessa forma, após fazer o checkout de uma tag antiga, recomendamos que adicione, na última linha do extends, o arquivo de versões do IDG compatível com aquela tag, presente no repositório https://github.com/plonegovbr/portalpadrao.release/.

Exemplo: você clonou o repositório do brasil.gov.portal na sua máquina, e deu checkout na tag 1.0.5. Ao editar o buildout.cfg, ficaria dessa forma, já com a última linha adicionada:

.. code-block:: cfg

    extends =
        https://raw.github.com/collective/buildout.plonetest/master/test-4.3.x.cfg
        https://raw.github.com/collective/buildout.plonetest/master/qa.cfg
        http://downloads.plone.org.br/release/1.0.4/versions.cfg
        https://raw.githubusercontent.com/plonegovbr/portal.buildout/master/buildout.d/versions.cfg
        https://raw.githubusercontent.com/plone/plone.app.robotframework/master/versions.cfg
        https://raw.githubusercontent.com/plonegovbr/portalpadrao.release/master/1.0.5/versions.cfg

Para saber qual arquivo de versões é compatível, no caso do brasil.gov.portal, é simples pois é a mesma versão (no máximo um bug fix, por exemplo, brasil.gov.portal é 1.1.3 e o arquivo de versão é 1.1.3.1). Para os demais pacotes, recomendamos comparar a data da tag do pacote e a data nos changelog entre uma versão e outra para adivinhar a versão compatível.

Tiles do pacote
---------------

Citação
^^^^^^^
Mostra uma citação de uma matéria.

.. figure:: https://raw.github.com/plonegovbr/brasil.gov.tiles/master/docs/quote.png
    :align: center
    :height: 250px
    :width: 530px

Foto do Dia
^^^^^^^^^^^
Mostra uma foto excepcional selecionada diariamente.

.. figure:: https://raw.github.com/plonegovbr/brasil.gov.tiles/master/docs/potd.png
    :align: center
    :height: 577px
    :width: 867px

Galeria de fotos
^^^^^^^^^^^^^^^^
Mostra uma galeria de fotos.

.. figure:: https://raw.github.com/plonegovbr/brasil.gov.tiles/master/docs/photogallery.png
    :align: center
    :height: 533px
    :width: 800px

Navegação
^^^^^^^^^
Mostra um menu de navegação exibindo os conteúdos como itens de menu a partir do caminho que foi adicionado.

.. figure:: https://raw.github.com/plonegovbr/brasil.gov.tiles/master/docs/navigation.png
    :align: center
    :height: 100px
    :width: 800px

Carrossel de grupo
^^^^^^^^^^^^^^^^^^
Mostra um carrossel de itens com imagens.

.. figure:: https://raw.github.com/plonegovbr/brasil.gov.tiles/master/docs/carousel.png
    :align: center
    :height: 393px


Desenvolvimento
---------------

Utilizamos `webpack <https://webpack.js.org/>`_ para gerenciar o conteúdo estático do tema,
tomando vantagem das diversas ferramentas e plugins disponíveis para suprir nossas necessidades.

Utilizamos a receita de buildout `sc.recipe.staticresources <https://github.com/simplesconsultoria/sc.recipe.staticresources>`_ para integrar o `webpack`_ no Plone.

Ao desenvolver os temas iniciamos o watcher do `webpack`_ e trabalhamos somente na pasta "webpack" alterando os arquivos;
o `webpack`_ se encarrega de processar e gerar os arquivos em seu endereço final.

Este pacote adiciona os seguintes comandos na pasta bin do buildout para processar automaticamente os recursos estáticos:

.. code-block:: console

    $ bin/env-brasilgovtiles

Este comando adiciona no terminal o node do buildout no PATH do sistema, dessa forma voce pode trabalhar com webpack conforme a documentação oficial.

.. code-block:: console

    $ bin/watch-brasilgovtiles

Este comando instrui ao Webpack para esperar por qualquer mudança nos arquivos SASS e gera a versão minificada do CSS para a aplicação.

.. code-block:: console

    $ bin/debug-brasilgovtiles

Este comando faz o mesmo que o comando watch, mas não minifica o CSS final.  Utilizado para debugar a geração do CSS.

.. code-block:: console

    $ bin/build-brasilgovtiles

Este comando cria o CSS minificado, mas não espera por mudanças.
