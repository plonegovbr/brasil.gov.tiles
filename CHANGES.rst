Changelog
---------

2.0a1 (unreleased)
^^^^^^^^^^^^^^^^^^

.. warning::
    Atualizações da branch 1.x do pacote só serão suportadas da versão mais recente dessa branch.
    Esta versão remove os tiles Banner rotativo, Carrossel de mídia, Em destaque e Social dos layouts existentes pois eles não são utilizados no IDG v2.
    Esta versão também remove os overrides dos tiles padrão do collective.cover e collective.nitf.
    Um processo de migração atualiza o atributo ``alt_text`` nesses tiles (o atributo ``variacao_titulo`` e simplesmente ignorado por ser um recurso que também não existe mais).

- Adiciona um tile para mostrar um Carrossel de destaques.
  [claytonc]

- Remove os tiles Banner rotativo, Carrossel de mídia, Em destaque e Social.
  [hvelarde]

- Adiciona um tile para mostrar um Carrossel de grupo.
  [claytonc]

- Remove override do tile de embed.
  [hvelarde]

- Usa o `six <https://pypi.python.org/pypi/six>`_ ao invés do ``future`` para compatibilidade futura com o Python 3.
  [hvelarde]

- Adiciona um tile para mostrar um Carrossel de vídeos.
  [rodfersou]

- Remove overrides dos tiles Banner e Básico do collective.cover.
  [hvelarde]

- Remove override do tile de matéria (collective.nitf).
  [hvelarde]

- Adiciona um tile para mostrar um menu de navegação.
  [claytonc]

- Adiciona um tile para mostrar uma Galeria de fotos.
  [claytonc]

- Adiciona um tile para mostrar a Foto do Dia.
  [claytonc, hvelarde]

- Adiciona um tile para mostrar uma citação de uma matéria.
  [rodfersou]

- Corrige dependências do pacote.
  [hvelarde]

- Adiciona suporte para processamento de recursos estáticos usando o `webpack <http://webpack.js.org/>`_.
  [rodfersou]

- Remove upgrade steps antigos.
  [rodfersou]
