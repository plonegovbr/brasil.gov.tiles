***************************
.gov.br: Blocos de Conteúdo
***************************

.. contents:: Conteúdo
   :depth: 2

Introdução
----------

Este complemento provê tiles (Blocos de conteúdo) para uso em sites Plone do Governo da República Federativa do Brasil.

Estado deste complemento
------------------------

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

Para habilitar a instalação deste produto em um ambiente que utilize o buildout:

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

4. Acesse o painel de controle e na opção **tiles** você verá os tiles providos por este pacote listados.

Atualização de 1.x a 2.x
------------------------

.. Warning::
    Só atualize para a versão 2.x do complemento depois de atualizar à versão mais recente da branch 1.x.
    O processo de migração remove os tiles descontinuados das capas existentes.

As atualizações da versão 1.x à 2.x só são suportadas das versões mais recentes de cada branch.
Antes de atualizar confira que você está efetivamente utilizando a última versão da branch 1.x e que não existem upgrade steps pendentes de serem aplicados.

Esta versão remove os tiles Banner rotativo, Carrossel de mídia, Destaque, Em destaque e Social dos layouts existentes pois eles não são utilizados no IDG v2.
**Esses tiles serão removidos das capas existentes.**

Esta versão também remove os overrides dos tiles padrão do collective.cover e collective.nitf.
Esses tiles serão migrados das capas existentes.
O processo de migração atualiza o atributo ``alt_text`` nesses tiles (o atributo ``variacao_titulo`` e simplesmente ignorado por ser um recurso que também não existe mais).

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


Carrossel de vídeos
^^^^^^^^^^^^^^^^^^^
Mostra um carrossel de vídeos.

.. figure:: https://raw.github.com/plonegovbr/brasil.gov.tiles/master/docs/videocarousel.png
    :align: center
    :height: 367px
    :width: 1253px

Carrossel de grupo
^^^^^^^^^^^^^^^^^^
Mostra um carrossel de itens com imagens.

.. figure:: https://raw.github.com/plonegovbr/brasil.gov.tiles/master/docs/groupcarousel.png
    :align: center
    :height: 393px
    :width: 800px

Carrossel de destaques
^^^^^^^^^^^^^^^^^^^^^^
Mostra um carrossel de imagens em destaques.

.. figure:: https://raw.github.com/plonegovbr/brasil.gov.tiles/master/docs/highlightscarousel.png
    :align: center
    :height: 550px
    :width: 1000px

Compartilhamento nas redes sociais
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Uma funcionalidade de compartilhamento nas redes sociais pode ser habilitada em alguns tiles seguindo os seguintes critérios:

Tile NITF
    Seu primeiro link aponte para um conteúdo interno.

Tile Rich Text
    É necessário que adicione alguma classe na configuração do tile (aba layout),
    e seu primeiro link aponte para um conteúdo interno.

.. figure:: https://raw.github.com/plonegovbr/brasil.gov.tiles/master/docs/tileshare.png
    :align: center
    :height: 713px
    :width: 1092px

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

Fazendo releases com o zest.releaser
------------------------------------

Os recursos estáticos do pacote são gerados usando o `webpack <https://webpack.js.org/>`_ e não são inclusos no VCS.
Se você está fazendo release usando o zest.releaser, você precisa fazer `upload manual dos arquivos no PyPI <https://github.com/zestsoftware/zest.releaser/issues/261>`_ ou você vai criar uma distribuição quebrada:

* execute ``longtest``, como de costume
* execute ``fullrelease``, como de costume, respondendo "não" a pergunta "Check out the tag?" para evitar o upload ao PyPI
* faça checkout na tag do release que você está liberando
* execute ``bin/build-brasilgovtemas`` para criar os recursos estáticos
* crie os arquivos da distribuição usando ``python setup.py sdist bdist_wheel``, como de costume
* faça o upload manual dos arquivos usando ``twine upload dist/*``

Em caso de erro você terá que criar um novo release pois o PyPI Warehouse `não permite reutilizar um nome de arquivo <https://upload.pypi.org/help/#file-name-reuse>`_.
