export var BannerRotativo = {
  init: function () {
    this.tileBannerRotativo();
    this.alturaBannerRotativo();
  },
  // Tile Banner Rotativo
  corrigeAlturaFaixa: function () {
    if ($(".template-compose #tile_banner_rotativo").length === 0) {
      let imgBannerRotativo    = $('#tile_banner_rotativo .activeSlide .banner img'),
        credito              = $('#tile_banner_rotativo .activeSlide .credito'),
        botoesBannerRotativo = $('#tile_banner_rotativo .button-nav');

      let sobrescrito = $('#tile_banner_rotativo').hasClass('chamada_sobrescrito');
      if (sobrescrito) {
        botoesBannerRotativo.css('top',
                                 imgBannerRotativo.height()         -
                                 botoesBannerRotativo.height()      +
                                 (credito ? credito.height() : 0)   -
                                 18);
      } else {
        botoesBannerRotativo.css('top',
                                 imgBannerRotativo.height()         -
                                 botoesBannerRotativo.height()      +
                                 (credito ? credito.height() : 0));
      }
    }
  },
  tileBannerRotativo: function () {
    if ($('#tile_banner_rotativo').length > 0) {
      $('#tile_banner_rotativo .button-nav, .orderTiles .button-nav').on('click focus mouseover', function (e) {
        e.preventDefault();
        $("#tile_banner_rotativo li").removeClass('activeSlide');
        $(this).closest('li').addClass('activeSlide');
        BannerRotativo.corrigeAlturaFaixa();
      });

      let updateCarrossel = function () {
        if (($('#tile_banner_rotativo a:hover').length === 0)   &&
            ($('#tile_banner_rotativo a:focus').length === 0)   &&
            ($(".template-compose #tile_banner_rotativo").length === 0)) {

          let totalSlides = $("#tile_banner_rotativo li").length;

          if (totalSlides > 1) {
            let activeSlide       = $('#tile_banner_rotativo li.activeSlide'),
              activeSlideNumber = parseInt(activeSlide.attr('data-slidenumber'), 10),
              nextSlideNumber   = (activeSlideNumber % totalSlides) + 1,
              nextSlide         = $('#banner' + nextSlideNumber);

            activeSlide.removeClass('activeSlide');
            nextSlide.addClass('activeSlide');
            BannerRotativo.corrigeAlturaFaixa();
          }
        }
        window.setTimeout(updateCarrossel, 4000);
      };
      window.setTimeout(updateCarrossel, 4000);
    }
  },
  resizeAlturaBannerRotativo: function () {
    if ($(".template-compose #tile_banner_rotativo").length === 0) {
      let containerBannerRotativo = $('#tile_banner_rotativo'),
        itemBannerRotativo = $('#tile_banner_rotativo li');

      let sobrescrito = $('#tile_banner_rotativo').hasClass('chamada_sobrescrito');

      // ajusta altura de cada item do banner
      let bannerMaior = 0;

      itemBannerRotativo.each(function () {
        let altura = ($(this).find('img')      ? $(this).find('img').height()      : 0)  +
                     ($(this).find('.credito') ? $(this).find('.credito').height() : 0)  +
                     ($(this).find('.title')   ? $(this).find('.title').height()   : 0)  +
                     ($(this).find('.descr')   ? $(this).find('.descr').height()   : 0);
        if (sobrescrito) {
          altura = altura - ($(this).find('.title')   ? $(this).find('.title').height()   : 0);
        }
        if (bannerMaior < altura) {
          bannerMaior = altura;
        }
      });
      itemBannerRotativo.css('height', bannerMaior);
      // ajusta altura do container do banner rotativo (22px = margin bottom default dos tiles)
      containerBannerRotativo.animate({'height': bannerMaior + 22}, 100, BannerRotativo.corrigeAlturaFaixa);
    }
  },
  alturaBannerRotativo: function () {
    $(window).resize(BannerRotativo.resizeAlturaBannerRotativo);
  }
};

export var BannerRotativoCompor = {
  init: function () {
    if ($('.template-compose #tile_banner_rotativo').length > 0) {
      this.removeObjFromTile();
      this.sortableTileItens();
    }
  },

  removeObjFromTile: function () {

    let objPortal = this;

    $("#tile_banner_rotativo a").click(function (e) {
      e.preventDefault();
    });

    $("#tile_banner_rotativo .tile-remove-item").remove();
    $("#tile_banner_rotativo").each(function () {
      let child = $(this).children('*[data-uuid]');
      child.append("<i class='tile-remove-item'><span class='text'>remove</span></i>");
    });

    $("#tile_banner_rotativo .tile-remove-item").unbind("click");
    $("#tile_banner_rotativo .tile-remove-item").click(function (e) {
      e.preventDefault();
      let obj = $(this).parent();
      let uuid = obj.attr("data-uuid");
      let tile = obj.parents('.tile');

      tile.find('.loading-mask').addClass('show remove-tile');
      let tile_type = tile.attr("data-tile-type");
      let tile_id = tile.attr("id");
      $.ajax({
        url: "@@removeitemfromlisttile",
        data: {'tile-type': tile_type, 'tile-id': tile_id, 'uuid': uuid},
        success: function (info) {
          tile.html(info);
          objPortal.titleMarkupSetup();
          tile.find('.loading-mask').removeClass('show remove-tile');
          return false;
        }
      });
    });
  },

  titleMarkupSetup: function () {
    $('#content .tile').each(function () {
      if ($(this).find('.loading-mask')[0] === undefined) {
        $(this).append('<div class="loading-mask"/>');
      }
    });
    this.removeObjFromTile();
  },

  sortableTileItens: function () {

    let objPortal = this;

    $("#tile_banner_rotativo").liveSortable({
      stop: function (event, ui) {
        let uuids = [];

        $(this).children().each(function (index) {
          if ($(this).attr("data-uuid") !== undefined) {
            uuids.push($(this).attr("data-uuid"));
          }
        });

        let tile = $(this).closest('.tile'),
          tile_type = tile.attr("data-tile-type"),
          tile_id = tile.attr("id");

        $.ajax({
          url: "@@updatelisttilecontent",
          data: {'tile-type': tile_type, 'tile-id': tile_id, 'uuids': uuids},
          success: function (info) {
            tile.html(info);
            objPortal.removeObjFromTile();
            return false;
          }
        });
      }
    });
  }
};