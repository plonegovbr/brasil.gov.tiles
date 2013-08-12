var portalBrasil = {
    init: function () {
        this.tileBannerRotativo();
    },
    // Tile Banner Rotativo
    tileBannerRotativo: function () {
        if ($('#banner_rotativo').length > 0) {
            $('#banner_rotativo .button-nav').click(function (e) {
                e.preventDefault();
                $('#banner_rotativo .button-nav').removeClass('activeSlide');
                $(this).addClass('activeSlide');
                $('#banner_rotativo .banner').removeClass('activeSlideItem');
                $(this).parent().find('.banner').addClass('activeSlideItem');
            });

            $('#banner_rotativo .button-nav').focus(function (e) {
                e.preventDefault();
                $('#banner_rotativo .button-nav').removeClass('activeSlide');
                $(this).addClass('activeSlide');
                $('#banner_rotativo .banner').removeClass('activeSlideItem');
                $(this).parent().find('.banner').addClass('activeSlideItem');
            });

            $('#banner_rotativo .button-nav').hover(function (e) {
                e.preventDefault();
                $('#banner_rotativo .button-nav').removeClass('activeSlide');
                $(this).addClass('activeSlide');
                $('#banner_rotativo .banner').removeClass('activeSlideItem');
                $(this).parent().find('.banner').addClass('activeSlideItem');
            });

            var updateCarrossel = function () {
                if (($('#banner_rotativo a:hover').length == 0) &&
                    ($('#banner_rotativo a:focus').length == 0)) {
                    var totalSlides = 4;
                    var activeSlide = $('#banner_rotativo .activeSlide');
                    var activeSlideItem = $('#banner_rotativo .activeSlideItem');
                    var activeSlideNumber = parseInt(activeSlide.html());
                    var nextSlideNumber = (activeSlideNumber % totalSlides) + 1;
                    var nextSlide = $('#banner' + nextSlideNumber + ' .button-nav');
                    var nextSlideItem = $('#banner' + nextSlideNumber + ' .banner');

                    $('#banner_rotativo .button-nav').removeClass('activeSlide');
                    $('#banner_rotativo .banner').removeClass('activeSlideItem');

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
