Changelog
---------

1.5.1 (2017-11-13)
^^^^^^^^^^^^^^^^^^

- Corrige bug no pache do banner rotativo que quebrava a remoção de itens nos demais tiles de lista (closes `#192 <https://github.com/plonegovbr/brasil.gov.tiles/issues/192>`_).
  [rodfersou]

- Corrige a edição de alguns tiles que não era exibidos após a edição de alguns campos títulos, rodapé, etc. (closes `#194 <https://github.com/plonegovbr/brasil.gov.tiles/issues/194>`_).
  [claytonc]


1.5 (2017-10-31)
^^^^^^^^^^^^^^^^

- Remove patch desnecessário em método ``_has_image_field()`` toda vez que a versão do collective.cover foi atualizada (closes `#170 <https://github.com/plonegovbr/brasil.gov.tiles/issues/170>`_).
  [hvelarde]

- Corrige o titulo do tile "Cabeçalho" que não era mostrado após a edição (closes `#144`)
  [claytonc]

- Substitui o tile poll do pacote pelo novo tile de collective.polls.
  [rodfersou]

- Remove 'five.grok' e plone.directives.form (closes `#185`)
  [caduvieira]


1.4rc1 (2017-10-05)
^^^^^^^^^^^^^^^^^^^

- Altera o tile de redes sociais para retirar o link das abas Facebook e Twitter para adequar a acessibilidade.
  [idgserpro]

- Altera o tile de notícia para corrigir o método alt que retornava sempre o valor True.
  [idgserpro]

- Altera o tile de notícia para não exibir links vazios quando não existir imagem a ser exibida.
  [idgserpro]


1.4b1 (2017-07-05)
^^^^^^^^^^^^^^^^^^

.. Warning::
    A versão necessária do collective.nitf para ser utilizada com esse pacote passa a ser >= 2.1b2.

- Tile de notícia (nitf) passa a herdar do tile criado no release 2.x de collective.nitf.
  [idgserpro]


1.3b1 (2017-07-03)
^^^^^^^^^^^^^^^^^^^

.. Warning::
    A versão necessária do collective.cover para ser utilizada com esse pacote
    passa a ser >= 1.3b1.

- Adapta brasil.gov.tiles para funcionar na versão mais atual de collective.cover,
  1.6b1.
  [idgserpro]


1.2rc1 (2017-06-23)
^^^^^^^^^^^^^^^^^^^

- Corrige exclusão e reordenação de itens de um Banner Rotativo com o uso de um
  patch. A correção definitiva deverá usar o tipo lista do collective.cover
  em outra versão.
  (partially closes `#145`)

- Segue o padrão do collective.cover de usar uuid ao invés de uid. (partially closes `#145`)
  [rodfersou, idgserpro]


1.2b1 (2016-11-07)
^^^^^^^^^^^^^^^^^^^

- Remove tile de carrossel para utilizar a tile do cover. (closes `#156`)
  [idgserpro]

- Adiciona plone4.csrffixes como dependência.
  [idgserpro]

- Adiciona plone.api como dependência.
  [idgserpro]

- Adicionando opção de link no título do cabeçalho do HeaderTile (closes `#157`).
  [caduvieira]


1.1rc1 (2016-06-09)
^^^^^^^^^^^^^^^^^^^

.. Warning::
    A estrutura de dados do tile "Destaque" foi alterada. Se você tiver algum
    tile desse tipo em sua capa, ele não será renderizado até que o upgradeStep
    de brasil.gov.tiles seja executado. Execute também os upgradeSteps de
    collective.cover uma vez que collective.cover não é mais pinado no
    buildout.cfg e as versões mais novas no momento desse release de
    brasil.gov.tiles contém upgrades.

- Corrige erro "Unexpected token <" quando se utiliza collective.cover com
  suporte a proteção CSRF.
  [idgserpro]

- Corrige ícones dos tiles presentes em overrides já que nas versões de
  collective.cover >= 1.1b1 a estrutura dos recursos estáticos foi alterada.
  (closes `#140`).
  [idgserpro]

- Corrige capa quebrada quando uma notícia (collective.nitf) sem imagem é
  adicionada num MediaCarouselTile. (closes `#136`).
  [idgserpro]

- Corrige teste quando se utiliza collective.cover 1.0a11 (closes `#132`).
  [idgserpro]


1.0.7 (2015-09-03)
^^^^^^^^^^^^^^^^^^
* Ajusta internacionalização nas strings de templates com traduções faltantes
  no domínio brasil.gov.tiles. (closes `#26`_).
  [idgserpro]
* Ajusta dicionário tamanhos de tile Nitf para português. (closes `#123`_).
  [dbarbato]


1.0.6 (2015-02-06)
^^^^^^^^^^^^^^^^^^
* Altera exibição de crédito para layouts de tile Banner Rotativo.
  [dbarbato]


1.0.5 (2014-12-06)
^^^^^^^^^^^^^^^^^^
* Adiciona testes para tiles de banner rotativo, basic e banner.
  [dbarbato]
* Ajusta code-analysis para produto.
  [dbarbato]
* Adiciona icones de tiles customizados via CSS.
  [dbarbato]
* Adiciona internacionalização i18n com suporte a Português e Espanhol. (closes `#120`_).
  [macagua]
* Updated Spanish a Brazilian Portuguese translations.
  [macagua]
* Added more improvements about i18n.
  [macagua]
* Replica ajuste do Rodrigo para espaçamento de Tile Banner de Portal Brasil.
  [dbarbato]
* Adiciona campo ALT em tile Basic, NITF e Banner conforme ajuste de rodfersou em
  Portal Brasil.
  [dbarbato]
* Adiciona novo layout de texto sobreposto no tile de Banner Rotativo.
  [dbarbato]


1.0.4 (2014-03-11)
^^^^^^^^^^^^^^^^^^
* Corrige carregamento de javascript (closes `#109`_).
  [rodfersou]
* Diminui altura mínima do Tile de Banner Rotativo.
  [dbarbato]
* Acerta registro de javascript.
  [dbarbato]


1.0.3 (2014-02-28)
^^^^^^^^^^^^^^^^^^
* Corrige carregamento do tile Media Carousel na home (closes `#107`_).
  [rodfersou]
* Oculta upgrade steps.
  [dbarbato]
* Cria tile Galeria de albuns (closes `#102`_).
  [rodfersou][felipeduardo]
* Desabilita testes robot executados pelo Travis (veja issue `#98`_) (closes `#99`_).
  [rodfersou]
* Melhora layout do tile Media Carousel (closes `#99`_).
  [rodfersou]
* Altera tile de Rede Social para português.
  [dbarbato]


1.0.2 (2013-12-12)
^^^^^^^^^^^^^^^^^^
* Correções na opção de esconder items no tile mediacarousel (aba layoutedit). Corrigida
  transição de slides para aumentar ou diminuir o tile conforme necessário.
  (closes `#96`_).
  [rodfersou]
* Revisado modo que os tiles são sobreescritos (closes `#91`_).
  [rodfersou]
* Removida dependência no unittest2.
  [hvelarde]
* Adicionadas dependências do pacote.
  [hvelarde]
* Revisado tamanho do footer dos tiles (closes `#88`_).
  [rodfersou][rennanrodrigues]
* Adicionada opção para variação de título nos tiles basic e
  basic news article (nitf) (closes `#86`_).
  [rodfersou]
* Adicionado suporte ao scale de imagem original (closes `#82`_).
  [rodfersou]


1.0.1 (2013-11-18)
^^^^^^^^^^^^^^^^^^^
* Acertando escala de imagem para banner rotativo.
  [dbarbato]
* Refatorado o banner rotativo (closes `#74`_).
  [rennanrodrigues]
* Tile banner rotativo ajustado para foto ter a proporção de 21x11,85 cm. (closes `#72`_).
  [rennanrodrigues]
* Correção de altura do container de navegação do media carousel (closes `#70`_).
  [rennanrodrigues]
* Correção de bug de altura e sobreposição de conteúdo no Tile de Redes Sociais (Twitter)
  (closes `#68`_).
  [rennanrodrigues]
* Correção de bug de transição do banner rotativo no layout de chamada com foto
  (closes `#65`_).
  [rennanrodrigues]


1.0 (2013-10-29)
^^^^^^^^^^^^^^^^^^^
* Removida a regra duplicada (closes `#63`_).
  [rennanrodrigues]
* Regra que estava no summary view para o tile collection (closes `#61`_).
  [rennanrodrigues]
* Regras de fonte do Tile collection (closes `#59`_).
  [rennanrodrigues]


1.0rc2 (2013-10-24)
^^^^^^^^^^^^^^^^^^^
* Front-end do novo banner rotativo  (closes `#57`_).
  [rennanrodrigues]
* Backend do novo banner rotativo  (closes `#57`_).
  [rodfersou]
* Inserção de estilos inline que estavam no template para o css dos tiles
  (closes `#53`_).
  [rennanrodrigues]
* Player da TV NBR ajustado para funcionar responsivo (closes `#55`_).
  [rennanrodrigues]
* Customização do código HTML gerado pelo player de audio (closes `#51`_).
  [rennanrodrigues]
* Removido atributo style do template de destaques (closes `#49`_).
  [rennanrodrigues]
* Revisado método de redimensionamento de imagens nos tiles (closes `#33`_).
  [rodfersou]
* Removido o atributo utilizado para abrir em nova aba os links;
  Implementação da tag <noscript> com mensagem de erro
  (closes `#46`_). [rennanrodrigues]
* Corrigido para não pré-carregar audio nos tiles audio e audiogallery
  (closes `#38`_).
  [rodfersou]
* Entre-linhas da descrição dos tiles de acordo com a arte (closes `#36`_).
  [rennanrodrigues]
* Revisão de fontes com fallbacks definidos (closes `#34`_).
  [rodfersou]
* Revisão de estilos da capa de editoria (closes `#31`_).
  [rennanrodrigues]
* Corrigido tile carousel para funcionar com itens que não possuem imagem,
  além de implementado re-scale de imagens segundo parametro da aba
  layout (closes `#27`_).
  [rodfersou]
* Correção no mediagallery para não dar mensagem de erro ao revisar tamanho
  dos galleries (closes `#28`_).
  [rodfersou]
* Revisão de referências entre tiles customizados (closes `#24`_).
  [rodfersou]
* Corrige configurações da Galeria de video.
  [ericof]
* Aumentada a altura mínima do elemento da galleria-container (closes `#7`_).
  [rennanrodrigues]
* Alterado para esconder o cabeçalho, título e descrição do player quando
  escondido na aba layout (closes `#7`_).
  [rodfersou]
* Removido espaçamento que estava sendo exibido quando não visualizando título
  e descrição (remoção de visualização por configs aba layout) (closes `#7`_).
  [rennanrodrigues]
* Alterado para não carregar conteúdo do tile embed na aba compor (closes `#20`_).
  [rodfersou]
* Retirado modo debug do mediacarousel (closes `#6`_).
  [rodfersou]
* Corrigido tile audiogallery para utilizar fallbacks de formato cadastrados
  no tipo Audio (closes `#16`_).
  [rodfersou]
* Corrigido tile audiogallery para tocar tipo de dados Audio (closes `#14`_).
  [rodfersou]
* Adicionado título no tile list (closes `#12`_).
  [rodfersou]
* Adicionado título no audio gallery (closes `#10`_).
  [rodfersou]
* Revisados headers selecionáveis para não quebrar caso o campo estiver oculto
  (closes `#8`_).
  [rodfersou]

1.0rc1 (2013-08-26)
^^^^^^^^^^^^^^^^^^^
* Implementação de funcionalidades drag & drop no Tile Banner rotativo
  [felipeduardo]
* Ajustes de CSS no Tile Media Carousel.
  [felipeduardo]
* Correção na altura do Facebook do Tile Social.
  [felipeduardo]
* Ajustes para Galeria de Vídeos em 1 Coluna.
  [felipeduardo]
* Atividade 319: Largura do Tile de Vídeo Fixa em 1 coluna.
  [rennanrodrigues]
* Atividade 198: Fonte na imagem do Banner Estático.
  [rennanrodrigues]
* Atividade 248: Deixar sempre visível o título do box Video Gallery
  [rodfersou]
* Atividade 294: Tile Collection.
  [rodfersou]
* Atividade 196: Adicionar funções no tile List.
  [rodfersou]
* Atividade 313: Título do Media Carousel - campo foi removido do 'compor'.
  [rodfersou]
* Tile de enquete sempre exibir form.
  [dbarbato]


1.0a1 (2013-07-22)
^^^^^^^^^^^^^^^^^^
* Versão inicial do pacote
  [ericof]

.. _`#6`: https://github.com/plonegovbr/brasil.gov.tiles/issues/6
.. _`#7`: https://github.com/plonegovbr/brasil.gov.tiles/issues/7
.. _`#8`: https://github.com/plonegovbr/brasil.gov.tiles/issues/8
.. _`#10`: https://github.com/plonegovbr/brasil.gov.tiles/issues/10
.. _`#12`: https://github.com/plonegovbr/brasil.gov.tiles/issues/12
.. _`#14`: https://github.com/plonegovbr/brasil.gov.tiles/issues/14
.. _`#16`: https://github.com/plonegovbr/brasil.gov.tiles/issues/16
.. _`#20`: https://github.com/plonegovbr/brasil.gov.tiles/issues/20
.. _`#24`: https://github.com/plonegovbr/brasil.gov.tiles/issues/24
.. _`#26`: https://github.com/plonegovbr/brasil.gov.tiles/issues/26
.. _`#27`: https://github.com/plonegovbr/brasil.gov.tiles/issues/27
.. _`#28`: https://github.com/plonegovbr/brasil.gov.tiles/issues/28
.. _`#31`: https://github.com/plonegovbr/brasil.gov.tiles/issues/31
.. _`#33`: https://github.com/plonegovbr/brasil.gov.tiles/issues/33
.. _`#34`: https://github.com/plonegovbr/brasil.gov.tiles/issues/34
.. _`#36`: https://github.com/plonegovbr/brasil.gov.tiles/issues/36
.. _`#38`: https://github.com/plonegovbr/brasil.gov.tiles/issues/38
.. _`#46`: https://github.com/plonegovbr/brasil.gov.tiles/issues/46
.. _`#49`: https://github.com/plonegovbr/brasil.gov.tiles/issues/49
.. _`#51`: https://github.com/plonegovbr/brasil.gov.tiles/issues/51
.. _`#53`: https://github.com/plonegovbr/brasil.gov.tiles/issues/53
.. _`#55`: https://github.com/plonegovbr/brasil.gov.tiles/issues/55
.. _`#57`: https://github.com/plonegovbr/brasil.gov.tiles/issues/57
.. _`#59`: https://github.com/plonegovbr/brasil.gov.tiles/issues/59
.. _`#61`: https://github.com/plonegovbr/brasil.gov.tiles/issues/61
.. _`#63`: https://github.com/plonegovbr/brasil.gov.tiles/issues/63
.. _`#65`: https://github.com/plonegovbr/brasil.gov.tiles/issues/65
.. _`#68`: https://github.com/plonegovbr/brasil.gov.tiles/issues/68
.. _`#70`: https://github.com/plonegovbr/brasil.gov.tiles/issues/70
.. _`#72`: https://github.com/plonegovbr/brasil.gov.tiles/issues/72
.. _`#74`: https://github.com/plonegovbr/brasil.gov.tiles/issues/74
.. _`#82`: https://github.com/plonegovbr/brasil.gov.tiles/issues/82
.. _`#86`: https://github.com/plonegovbr/brasil.gov.tiles/issues/86
.. _`#88`: https://github.com/plonegovbr/brasil.gov.tiles/issues/88
.. _`#91`: https://github.com/plonegovbr/brasil.gov.tiles/issues/91
.. _`#96`: https://github.com/plonegovbr/brasil.gov.tiles/issues/96
.. _`#99`: https://github.com/plonegovbr/brasil.gov.tiles/issues/99
.. _`#98`: https://github.com/plonegovbr/brasil.gov.tiles/issues/98
.. _`#102`: https://github.com/plonegovbr/brasil.gov.tiles/issues/102
.. _`#107`: https://github.com/plonegovbr/brasil.gov.tiles/issues/107
.. _`#109`: https://github.com/plonegovbr/brasil.gov.tiles/issues/109
.. _`#120`: https://github.com/plonegovbr/brasil.gov.tiles/issues/120
.. _`#123`: https://github.com/plonegovbr/brasil.gov.tiles/issues/123
.. _`#132`: https://github.com/plonegovbr/brasil.gov.tiles/issues/132
.. _`#136`: https://github.com/plonegovbr/brasil.gov.tiles/issues/136
.. _`#140`: https://github.com/plonegovbr/brasil.gov.tiles/issues/140
.. _`#145`: https://github.com/plonegovbr/brasil.gov.tiles/issues/145
.. _`#156`: https://github.com/plonegovbr/brasil.gov.tiles/issues/156
