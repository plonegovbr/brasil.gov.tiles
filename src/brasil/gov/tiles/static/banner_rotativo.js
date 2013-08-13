var portalBrasil = {
    init: function () {
        this.tileBannerRotativo();
    },
    // Tile Banner Rotativo
    tileBannerRotativo: function () {
        if ($('#tile_banner_rotativo').length > 0) {

            $('#tile_banner_rotativo .button-nav').on('click',function (e) {
                e.preventDefault();
                $('#tile_banner_rotativo .button-nav').removeClass('activeSlide');
                $(this).addClass('activeSlide');
                $('#tile_banner_rotativo .banner').removeClass('activeSlideItem');
                $(this).parent().find('.banner').addClass('activeSlideItem');
            }).on('focus',function (e) {
                e.preventDefault();
                $('#tile_banner_rotativo .button-nav').removeClass('activeSlide');
                $(this).addClass('activeSlide');
                $('#tile_banner_rotativo .banner').removeClass('activeSlideItem');
                $(this).parent().find('.banner').addClass('activeSlideItem');
            }).on('mouseover',function (e) {
                e.preventDefault();
                $('#tile_banner_rotativo .button-nav').removeClass('activeSlide');
                $(this).addClass('activeSlide');
                $('#tile_banner_rotativo .banner').removeClass('activeSlideItem');
                $(this).parent().find('.banner').addClass('activeSlideItem');
            });

            var updateCarrossel = function () {
                if (($('#tile_banner_rotativo a:hover').length == 0) &&
                    ($('#tile_banner_rotativo a:focus').length == 0)) {
                    var totalSlides = 4;
                    var activeSlide = $('#tile_banner_rotativo .activeSlide');
                    var activeSlideItem = $('#tile_banner_rotativo .activeSlideItem');
                    var activeSlideNumber = parseInt(activeSlide.html());
                    var nextSlideNumber = (activeSlideNumber % totalSlides) + 1;
                    var nextSlide = $('#banner' + nextSlideNumber + ' .button-nav');
                    var nextSlideItem = $('#banner' + nextSlideNumber + ' .banner');

                    $('#tile_banner_rotativo .button-nav').removeClass('activeSlide');
                    $('#tile_banner_rotativo .banner').removeClass('activeSlideItem');

                    nextSlide.addClass('activeSlide');
                    nextSlideItem.addClass('activeSlideItem');
                }

                window.setTimeout(updateCarrossel, 4000);
            }
            window.setTimeout(updateCarrossel, 4000);
        }
    }
};

$(function () {
    "use strict";
    portalBrasil.init();
});
