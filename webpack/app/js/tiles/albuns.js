let cycle2_loaded = null;

// Tile Galeria de Albuns
let Albuns = {
  // View de álbum carrossel (carrossel de imagens do álbum)
  carrossel: function () {
    if (!cycle2_loaded) {
      cycle2_loaded = true;

      var obj = this;
      $('.cycle-slideshow').on('cycle-next cycle-prev', function (e, opts) {
        var $galeria = $(this).parent().parent();
        var $slideshows = $('.cycle-slideshow', $galeria);
        $slideshows.not(this).cycle('goto', opts.currSlide);
        obj.layoutAdjustment($galeria, opts.currSlide);
      });

      // Aplicando o mesmo controle de navegacao para os thumbs e galerias
      $('.cycle-carrossel .thumb-itens').click(function (e){
        e.preventDefault();
        var $thumbs = $(this).parent().parent();
        var $galeria = $thumbs.parent().parent();
        var $slideshows = $('.cycle-slideshow', $galeria);
        var index = $thumbs.data('cycle.API').getSlideIndex(this);
        $slideshows.cycle('goto', index);
        obj.layoutAdjustment($galeria, index);
      });

      // Adicionando navegação por teclado
      $(document.documentElement).keyup(function (event) {
        if (event.keyCode == 37) {
          $('.cycle-prev').trigger('click');
        } else if (event.keyCode == 39) {
          $('.cycle-next').trigger('click');
        }
      });

      $('.cycle-slideshow').each(function(){
        var $galeria = $(this).parent().parent();
        obj.layoutAdjustment($galeria, 0);
      });
    }
  },

  layoutAdjustment: function($galeria, index){
    var aElem = $(".cycle-player .cycle-slide", $galeria),
      elem,
      novaaltura,
      alturaimagem,
      larguracarosel;

    // Pula primeiro elemento
    index = index + 1;
    elem = aElem[index],
      novaaltura = $(elem).height();
    alturaimagem = $('.cycle-sentinel img', $galeria).height();
    larguracarosel = ($('.carousel', $galeria).width() -
      (36 * 2));

    $('.cycle-sentinel', $galeria).height(novaaltura);
    $('.cycle-hover', $galeria).height(alturaimagem);
    $('.cycle-carrossel', $galeria).width(larguracarosel);
  }
};


export default Albuns;
