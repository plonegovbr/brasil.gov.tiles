let instance = null;


let CarouselResponsiveResize = function () {
  let _Singleton = (function () {
    function _Singleton() {}

    _Singleton.prototype.qtd_coluna_anterior = '';
    _Singleton.prototype.scrollbar = false;

    _Singleton.prototype.resize = function () {
      let qtd_coluna_atual;

      qtd_coluna_atual = 1;

      if ($(window).width() > 480) {
        qtd_coluna_atual = 2;
      }

      // 3 columns, 460 + 30 padding
      if ($(window).width() > 960) {
        qtd_coluna_atual = 3;
      }

      if (this.qtd_coluna_anterior !== qtd_coluna_atual) {
        this.qtd_coluna_anterior = qtd_coluna_atual;
        let _i, _len;
        let gallerias = Galleria.get();

        for (_i = 0, _len = gallerias.length; _i < _len; _i++) {
          let g = gallerias[_i];
          if (g) {
            let mediacarousel = '#' + g._target.id;
            g.resize({
              width: g._stageWidth,
              height: g._stageWidth*3/4
            });
            $(mediacarousel).css({
              height: g._stageWidth*3/4
            });

            let bottomThumbs = $('.galleria-thumbnails-container', mediacarousel).offset().top +
              $('.galleria-thumbnails-container', mediacarousel).height();
            let bottomContainer = $(mediacarousel).offset().top +
              $(mediacarousel).height();
            let heightContainer = $(mediacarousel).height() +
              (bottomThumbs             -
              bottomContainer)         +
              ($(mediacarousel+' + .mediacarousel-footer-container a').text === '' ? 39: 18) +
              8;
            $(mediacarousel).css({
              height: heightContainer
            });
            let tile = $(mediacarousel).parent().parent();
            $('.loading-mask', tile).css({
              height: tile.height() + 15
            });
          }
        }
      }
    };

    return _Singleton;
  })();

  if (instance == null) {
    instance = new _Singleton();
  }
  return instance;
};


function MediaCarousel(mediacarousel) {
  var self = this,
    galleria_id = mediacarousel.attr('id');

  $.extend(self, {
    init: function(){
      Galleria.loadTheme(window.location.protocol + '//' + window.location.host + location.pathname + '/++resource++brasil.gov.tiles/vendor/galleria.classic.min.js');

      Galleria.configure({
        _toggleInfo: false, // Set this to false if you want the caption to show always
        debug      : false, // Set this to false to prevent debug messages
        imageCrop  : false, // Defines how Galleria will crop the image
        wait       : true,  // Defines if and how Galleria should wait until it can be displayed using user interaction
        responsive : false  // This option sets thew Gallery in responsive mode
      });

      Galleria.on('image', function(e) {
        var mediacarousel = '#'+this._target.id;

        // Sometimes (I don't know why) Galleria fails, so I need to check if it worked and remove duplicates
        if (($('.galleria-layer>.rights', mediacarousel).length > 0) &&
          ($('.galleria-info-text>.rights[data-index='+e.index+']', mediacarousel).length > 0)) {
          $('.galleria-info-text>.rights[data-index='+e.index+']', mediacarousel).remove();
        }

        // Move the layer element to the right place
        if ($('.galleria-layer>.rights', mediacarousel).length > 0) {
          $('.galleria-info-text', mediacarousel).append($('.galleria-layer>.rights', mediacarousel));
        }

        // Sometimes (I don't know why) Galleria fails, so I need to check if it worked and hide duplicates
        if ($('.galleria-info-text>.rights[data-index='+e.index+']', mediacarousel).length > 0) {
          $('.rights', mediacarousel).each(function(){
            $(this).css('display', 'none');
          });
          $('.galleria-info-text>.rights[data-index='+e.index+']', mediacarousel).css('display', 'block');
        }

        $('.galleria-thumbnails-container', mediacarousel).insertAfter($('.galleria-info', mediacarousel));
        var bottomThumbs = $('.galleria-thumbnails-container', mediacarousel).offset().top +
          $('.galleria-thumbnails-container', mediacarousel).height();
        var bottomContainer = $(mediacarousel).offset().top +
          $(mediacarousel).height();
        var heightContainer = $(mediacarousel).height() +
          (bottomThumbs             -
          bottomContainer)         +
          ($(mediacarousel+' + .mediacarousel-footer-container a').text === '' ? 39: 18) +
          8;

        if (!$(mediacarousel).hasClass('image')){
          $(mediacarousel).addClass('image');
          $(mediacarousel).animate({
            height: heightContainer
          });
          $('.galleria-thumbnails-container, .galleria-info').animate({
            opacity: 1
          }, function () {
            var tile = $(mediacarousel).parent().parent();
            $('.loading-mask', tile).css({
              height: tile.height() + 15
            });
          });
        }
      });
      Galleria.on('loadfinish', function(e) {
        var mediacarousel = '#'+this._target.id;
        $('.galleria-thumbnails-container', mediacarousel).insertAfter($('.galleria-info', mediacarousel));
        var bottomThumbs = $('.galleria-thumbnails-container', mediacarousel).offset().top +
          $('.galleria-thumbnails-container', mediacarousel).height();
        var bottomContainer = $(mediacarousel).offset().top +
          $(mediacarousel).height();
        var heightContainer = $(mediacarousel).height() +
          (bottomThumbs             -
          bottomContainer)         +
          ($(mediacarousel+' + .mediacarousel-footer-container a').text === '' ? 39: 18) +
          8;

        var tile           = $(mediacarousel).parent().parent(),
          thumbGaleria   = $('.galleria-thumbnails-list', tile),
          navGaleriaNext = $('.galleria-thumb-nav-right', tile);
        if (navGaleriaNext.hasClass('disabled')) {
          thumbGaleria.css({ 'margin-right': 10 });
        } else {
          thumbGaleria.css({ 'margin-right': 40 });
        }
        if ($(mediacarousel).hasClass('image')) {
          $(mediacarousel).css({
            height: heightContainer
          });
          var tile = $(mediacarousel).parent().parent();
          $('.loading-mask', tile).css({
            height: tile.height() + 15
          });
        }
      });
      Galleria.run('#'+galleria_id);

      Galleria.ready(function() {
        var galleriaContainer = $('#'+this._target.id),
          tile = $(galleriaContainer).parent().parent();
        if (!galleriaContainer.hasClass('ready')) {
          galleriaContainer.addClass('ready');
          var galleriaContainerWidth  = galleriaContainer.width(),
            galleriaContainerHeight = (galleriaContainerWidth*3)/4;
          this.resize({
            width: galleriaContainerWidth,
            height: galleriaContainerHeight
          });
        }
        $('.galleria-thumb-nav-left, .galleria-thumb-nav-right, .galleria-thumbnails .galleria-image img', tile).on('click', function() {
          var thumbGaleria   = $('.galleria-thumbnails-list', tile),
            navGaleriaNext = $('.galleria-thumb-nav-right', tile);
          if (navGaleriaNext.hasClass('disabled')) {
            thumbGaleria.css({ 'margin-right': 10 });
          } else {
            thumbGaleria.css({ 'margin-right': 40 });
          }
        });
      });
    },
  });
  self.init();
}

$.fn.mediacarousel = function() {

  // already instanced, return the data object
  var el = this.data("mediacarousel");
  if (el) { return el; }

  var default_settings = this.data('mediacarousel-settings');

  return this.each(function() {
    el = new MediaCarousel($(this));
    $(this).data("mediacarousel", el);

  });
};

$(document).on(
  'submit',
  'form[action*=edit-tile\\/mediacarousel]',
  function(){
    setTimeout(function() {
      location.reload();
    }, 400);
  }
);


export default CarouselResponsiveResize;
