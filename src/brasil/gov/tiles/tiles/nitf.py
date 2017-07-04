# -*- coding: utf-8 -*-
from brasil.gov.tiles import _ as _
from collective.cover.tiles.configuration_view import IDefaultConfigureForm
from collective.nitf.tiles.nitf import INITFTile
from collective.nitf.tiles.nitf import NITFTile
from plone.autoform import directives as form
from zope import schema
from zope.browserpage import ViewPageTemplateFile


class INITFBasicTile(INITFTile):
    """A tile that shows general information about news articles.
    """

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

    def variacao_titulo(self):
        tamanhos = {
            u'Normal': None,
            u'Grande': 'grande',
            u'Gigante': 'gigante'
        }
        if self.data['variacao_titulo']:
            return tamanhos[self.data['variacao_titulo']]

    @property
    def title_tag(self):
        """Customizamos esse método que já existe em NITFTile para podermos
        utilizar a lógica presente em brasil.gov.tiles de variacao_titulo."""
        field = self._get_field_configuration('title')
        tag, title, href = field['htmltag'], field['content'], self.getURL()
        if self.variacao_titulo() and tag == 'h2':
            tag = '{0} class="{1}"'.format(tag, self.variacao_titulo())
        if href:
            return u'<{tag}><a href="{href}">{title}</a></{tag}>'.format(
                tag=tag, href=href, title=title)
        else:
            # in HTML5 the href attribute may be omitted (placeholder link)
            return u'<{tag}><a>{title}</a></{tag}>'.format(tag=tag, title=title)
