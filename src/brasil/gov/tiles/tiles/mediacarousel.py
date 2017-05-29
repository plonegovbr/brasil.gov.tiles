# -*- coding: utf-8 -*-

from brasil.gov.tiles import _ as _
from collective.cover.tiles.configuration_view import IDefaultConfigureForm
from collective.cover.tiles.list import IListTile
from collective.cover.tiles.list import ListTile
from plone.autoform import directives as form
from plone.namedfile.field import NamedBlobImage as NamedImage
from plone.tiles.interfaces import ITileDataManager
from Products.CMFPlone.utils import safe_hasattr
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.interface import implementer


class IMediaCarouselTile(IListTile):
    """
    """

    # FIXME: Ver como migrar NamedImage para NamedBlobImage, como está previsto
    # em https://github.com/collective/collective.cover/blob/1.1b1/src/collective/cover/tiles/list.py#L66
    form.omitted('image')
    form.no_omit(IDefaultConfigureForm, 'image')
    image = NamedImage(
        title=_(u'Image'),
        required=False,
        readonly=True,
    )

    # Apesar do nome, footer_text contém o LINK e não o texto do link.
    # FIXME: Esse campo poderia deixar de existir para começar a ser usado o
    # more_link do collective.cover.tiles.list, mas ele está com problemas.
    # Ver https://github.com/collective/collective.cover/issues/708
    # Quando o issue for resolvido e esse campo for removido não esqueça do
    # upgradeStep, utilize como base o que foi feito no campo header presente
    # em upgrades/v4002/upgrades_tile_carrossel_multimidia
    # Como o erro ainda não foi corrigido, o campo problemático precisa ser
    # escondido via css, pois defini-lo aqui como form.ommited('campo') não
    # funciona. Tentar especificar o campo aqui nessa classe e na sequência
    # colocar form.ommited também não funciona, sobrando apenas o recurso de
    # esconder via css.
    footer_text = schema.TextLine(
        title=_(u'Footer Link'),
        required=False,
        readonly=False,
    )


@implementer(IMediaCarouselTile)
class MediaCarouselTile(ListTile):
    index = ViewPageTemplateFile('templates/mediacarousel.pt')
    short_name = _(u'Media Carousel', default=u'Media Carousel')

    def populate_with_object(self, obj):
        super(MediaCarouselTile, self).populate_with_object(obj)
        # XXX: Customizamos esse método apenas para poder atribuir ao título
        # do tile o mesmo título de uma coleção/folder que for aplicado assim
        # como o footer_text. Não seria o caso de propor para isso ser
        # incorporado ao próprio cover? # Ou seja, se num tile, cujo
        # accepted_ct aceita tipos "container" ou collection, pegar o title e a
        # url do container (no caso do collective.cover, ao invés de
        # 'footer_text' seria more_link)? A se estudar.
        data_mgr = ITileDataManager(self)
        old_data = data_mgr.get()
        old_data['tile_title'] = obj.Title()
        old_data['footer_text'] = obj.absolute_url()
        data_mgr.set(old_data)

    def thumbnail(self, item):
        if self._has_image_field(item):
            scales = item.restrictedTraverse('@@images')
            return scales.scale('image', width=80, height=60)

    def scale(self, item):
        # TODO: Podemos usar o método scale presente em
        # https://github.com/collective/collective.cover/blob/1.1b1/src/collective/cover/tiles/base.py#L384
        # Estudar.
        if self._has_image_field(item):
            scales = item.restrictedTraverse('@@images')
            return scales.scale('image', width=692, height=433)

    def accepted_ct(self):
        """ Return a list of content types accepted by the tile.
        """
        return ['Collection', 'Folder']

    def get_media_url(self, obj):
        portal_type = obj.getPortalTypeName()
        url = ''
        if portal_type == 'sc.embedder':
            url = obj.url
        elif portal_type == 'Image':
            url = obj.absolute_url() + '/@@images/image'
        elif portal_type == 'collective.nitf.content':
            scale = self.scale(obj)
            if scale is not None:
                url = scale.url
            else:
                url = obj.absolute_url()

        return url

    def get_rights(self, obj):
        rights = obj.Rights() if safe_hasattr(obj, 'Rights') else None
        if rights is not None:
            return rights
        return ''

    def show_tile_title(self):
        # FIXME: Não deveríamos alterar direto em collective.cover para que,
        # no método
        # https://github.com/collective/collective.cover/blob/1.1b1/src/collective/cover/tiles/list.py#L343
        # ele já verificasse se está visível e já retornasse o valor do
        # atributo?
        return self._field_is_visible('tile_title')

    def get_title(self, item):
        # TODO: Estudar para ver se podemos usar o get_title_tag de
        # https://github.com/collective/collective.cover/blob/1.1b1/src/collective/cover/tiles/list.py#L382
        # e remover esse método daqui.
        title = ''
        if self._field_is_visible('title'):
            title = '<a href="' + item.absolute_url() + '/view">' + item.title + '</a>'
        return title

    def get_description(self, item):
        description = ''
        if self._field_is_visible('description'):
            description = item.Description()
        return description

    def get_configured_fields(self):
        """
        Em tese, não preciso desse método customizado aqui: sua definição em
        https://github.com/collective/collective.cover/blob/1.1b1/src/collective/cover/tiles/list.py#L274
        utiliza o getFieldsInOrder o que, em tese, já iria trazer os campos na
        ordem correta.

        Acontece que, ao herdarmos diretamente da lista do collective.cover,
        removemos vários campos devido à redundância dos mesmos e, com isso,
        a ordem fica imprevisível. Então utilizamos esse método para ir na
        ordem mais correta.

        Ex: Esse era o schema:

            header = schema.TextLine
            title = schema.TextLine
            image = NamedImage
            uuids = schema.List
            footer_text = schema.TextLine

        Mas vem assim do get_configured_fields:

            {'id': 'uuids', 'title': u'Elements'}
            {'id': 'count', 'title': u'Number of items to display'}
            {'id': 'title', 'htmltag': u'h2', 'title': u'Title'}
            {'id': 'description', 'title': u'Description'}
            {'format': 'datetime', 'id': 'date', 'title': u'Date'}
            {'id': 'tile_title', 'htmltag': u'h2', 'title': u'Tile Title'}
            {'id': 'more_link', 'htmltag': u'h2', 'title': u'Show more... link'}
            {'id': 'more_link_text', 'htmltag': u'h2', 'title': u'Show more... link text'}
            {'scale': u'mini 200:200', 'id': 'image', 'title': u'Image'}
            {'id': 'footer_text', 'htmltag': u'h2', 'title': u'Footer Link'}
            {'id': 'css_class', 'title': u'CSS Class'}

        videogallery e audiogallery tambem usam o get_configured_fields, mas
        basicamente apenas pro título do tile então esse método não está
        presente por lá. No futuro pode-se até em pensar em refatorá-los,
        hoje está assim para manter o padrão do tipo lista.

        """
        order = [
            'tile_title', 'title', 'image', 'uuids', 'footer_text', 'more_link',
            'count', 'description', 'date', 'more_link_text', 'footer_text',
            'css_class'
        ]
        get_configured_fields = super(MediaCarouselTile, self).get_configured_fields()
        return sorted(get_configured_fields, key=lambda x: order.index(x['id']))

    def results(self):
        valid_portal_types = ['sc.embedder', 'Image', 'collective.nitf.content']
        return super(MediaCarouselTile, self).results(portal_type=valid_portal_types)

    def init_js(self):
        return """
$(document).ready(function() {
    $('#mediacarousel-gallerie-%s').mediacarousel();
});
""" % (self.id)
