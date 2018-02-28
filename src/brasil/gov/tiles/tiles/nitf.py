# -*- coding: utf-8 -*-
from brasil.gov.tiles import _ as _
from collective.cover.tiles.configuration_view import IDefaultConfigureForm
from collective.nitf.tiles.nitf import INITFTile
from collective.nitf.tiles.nitf import NITFTile
from plone.autoform import directives as form
from plone.tiles.interfaces import ITileDataManager
from zope import schema
from zope.browserpage import ViewPageTemplateFile


class INITFBasicTile(INITFTile):
    """A tile that shows general information about news articles.
    """

    # FIXME: Há interesse de colocar esse campo no collective.cover, mas ainda
    # sem previsão.
    # https://github.com/plonegovbr/brasil.gov.tiles/pull/178#issuecomment-313092733
    # A partir da versão 1.3b2, com a atualização do collective.nitf para 2.x e
    # com o tile de NITF passando a herdar do tile de collective.nitf ao invés
    # do basic em brasil.gov.tiles, esse atributo foi perdido e por isso ele
    # foi adicionado aqui.
    form.no_omit('image_description')
    form.omitted(IDefaultConfigureForm, 'image_description')
    image_description = schema.TextLine(
        title=_(u'ALT'),
        required=False,
    )

    form.no_omit('variacao_titulo')
    form.omitted(IDefaultConfigureForm, 'variacao_titulo')
    variacao_titulo = schema.Choice(
        title=_(u'Change in Title'),
        values=(u'Normal',
                u'Grande',
                u'Gigante'),
        default=u'Normal',
        required=True,
    )


class NITFBasicTile(NITFTile):
    """A tile that shows general information about news articles.
    """
    short_name = _(u'Basic News Article Tile', u'Basic News Article Tile')

    # TODO: Estudar, no futuro, se realmente precisamos dessa template
    # customizada. A principal motivação de continuar com esse tile é o método
    # variacao_titulo, e a funcionalidade disso foi adicionada no método
    # title_tag, sendo chamado em nitf.pt no próprio collective.nitf.
    # É importante alguém especialista em css fazer essa análise, pois o
    # posicionamento dos elementos de brasil.gov.tiles/nitf.pt é diferente dos
    # presentes em collective.nitf/tiles.pt.
    index = ViewPageTemplateFile('templates/nitf.pt')

    def populate_with_object(self, obj):
        """
        FIXME:

        Método customizado para dar suporte ao campo 'image_description'.

        Adaptado de

        https://github.com/plonegovbr/brasil.gov.tiles/blob/1.2rc1/src/brasil/gov/tiles/tiles/nitf.py#L49
        """
        super(NITFBasicTile, self).populate_with_object(obj)
        data_mgr = ITileDataManager(self)
        data = data_mgr.get()
        img = obj.getImage()
        if img:
            data['image_description'] = img.Description() or img.Title()
        data_mgr.set(data)

    def variacao_titulo(self):
        tamanhos = {
            u'Normal': None,
            u'Grande': 'grande',
            u'Gigante': 'gigante',
        }
        if self.data['variacao_titulo']:
            return tamanhos[self.data['variacao_titulo']]

    @property
    def alt(self):
        """
        FIXME:
        Copiado de

        https://github.com/collective/collective.cover/blob/6621363f0228e3dbf94ca26c786eddd690fc6c68/src/collective/cover/tiles/basic.py#L140

        Essa cópia só é necessária porque ainda temos o atributo 'image_description'.
        Se um dia for incorporado no upstream do collective.cover e o método alt
        de lá passar a fazer o que esse faz, isso aqui pode ser removido.

        Foi adaptado para seguir a idéia de

        https://github.com/plonegovbr/brasil.gov.tiles/blob/caa250e9c3428d000174368321c42dae2fb48f92/src/brasil/gov/tiles/tiles/basic.py#L160
        """
        return self.data.get('image_description') or self.data.get('description') or self.data.get('title')

    @property
    def title_tag(self):
        """
        Customizamos esse método que já existe em NITFTile para podermos
        utilizar a lógica presente em brasil.gov.tiles de variacao_titulo.

        Adaptado de

        https://github.com/collective/collective.nitf/blob/8543e179d21e2ae1e1d525ae660b882e2d8b79d3/src/collective/nitf/tiles/nitf.py
        """
        field = self._get_field_configuration('title')
        tag, title, href = field['htmltag'], field['content'], self.getURL()
        # inicio customizacao variacao_titulo
        if self.variacao_titulo() and tag == 'h2':
            tag = '{0} class="{1}"'.format(tag, self.variacao_titulo())
        # fim customizacao variacao_titulo
        if href:
            return u'<{tag}><a href="{href}">{title}</a></{tag}>'.format(
                tag=tag, href=href, title=title)
        else:
            # in HTML5 the href attribute may be omitted (placeholder link)
            return u'<{tag}><a>{title}</a></{tag}>'.format(tag=tag, title=title)
