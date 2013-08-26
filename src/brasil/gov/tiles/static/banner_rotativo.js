var portalBrasil = {
    init: function () {
        this.tileBannerRotativo();
    },
    // Tile Banner Rotativo
    tileBannerRotativo: function () {
        if ($('#tile_banner_rotativo').length > 0) {

            $('#tile_banner_rotativo .button-nav, .orderTiles .button-nav').on('click focus mouseover',function (e) {
                e.preventDefault();
                $('#tile_banner_rotativo .button-nav').removeClass('activeSlide');
                $(this).addClass('activeSlide');
                $('#tile_banner_rotativo .banner').removeClass('activeSlideItem');
                $(this).parent().find('.banner').addClass('activeSlideItem');
            });

            var updateCarrossel = function () {
                if (($('#tile_banner_rotativo a:hover').length == 0) &&
                    ($('#tile_banner_rotativo a:focus').length == 0) &&
                    ($(".template-compose #tile_banner_rotativo").length == 0)){

                    var iTotalSlides = $("#tile_banner_rotativo li").length;

                    var totalSlides = iTotalSlides,
                        activeSlide = $('#tile_banner_rotativo .activeSlide'),
                        activeSlideItem = $('#tile_banner_rotativo .activeSlideItem'),
                        activeSlideNumber = parseInt(activeSlide.html()),
                        nextSlideNumber = (activeSlideNumber % totalSlides) + 1;

                    var nextSlide = $('#banner' + nextSlideNumber + ' .button-nav'),
                        nextSlideItem = $('#banner' + nextSlideNumber + ' .banner');

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

var portalBrasilCompor = {
    init: function () {
        if ($('.template-compose #tile_banner_rotativo').length > 0){
            this.removeObjFromTile();
            this.sortableTileItens();
        }
    },

    removeObjFromTile: function(){

        var objPortal = this;

        $("#tile_banner_rotativo a").click(function(e) {
            e.preventDefault();
        });

        $("#tile_banner_rotativo .tile-remove-item").remove();
        $("#tile_banner_rotativo").each(function(){
            var child = $(this).children('*[data-uid]');
            child.append("<i class='tile-remove-item'><span class='text'>remove</span></i>");
        });

        $("#tile_banner_rotativo .tile-remove-item").unbind("click");
        $("#tile_banner_rotativo .tile-remove-item").click(function(e) {
            e.preventDefault();
            var obj = $(this).parent();
            uid = obj.attr("data-uid");
            var tile = obj.parents('.tile');

            tile.find('.loading-mask').addClass('show remove-tile');
            var tile_type = tile.attr("data-tile-type");
            var tile_id = tile.attr("id");
            $.ajax({
                 url: "@@removeitemfromlisttile",
                 data: {'tile-type': tile_type, 'tile-id': tile_id, 'uid': uid},
                 success: function(info) {
                     tile.html(info);
                     objPortal.titleMarkupSetup();
                     tile.find('.loading-mask').removeClass('show remove-tile');
                     return false;
                 }
            });
        });
    },

    titleMarkupSetup: function(){
        $('#content .tile').each(function(){
            if ($(this).find('.loading-mask')[0] === undefined) {
                $(this).append('<div class="loading-mask"/>');
            }
        });
        this.removeObjFromTile();
    },

    sortableTileItens: function(){

        var objPortal = this;

        $("#tile_banner_rotativo").liveSortable({
            stop:function(event, ui) {
                var uids = [];

                $(this).children().each(function(index) {
                    if ($(this).attr("data-uid") !== undefined) {
                        uids.push($(this).attr("data-uid"));
                    }
                });

                var tile = $(this).closest('.tile'),
                    tile_type = tile.attr("data-tile-type"),
                    tile_id = tile.attr("id");

                $.ajax({
                     url: "@@updatelisttilecontent",
                     data: {'tile-type': tile_type, 'tile-id': tile_id, 'uids': uids},
                     success: function(info) {
                         tile.html(info);
                         objPortal.removeObjFromTile();
                         return false;
                     }
                 });
            }
        });

    }
};

$(function () {
    "use strict";
    portalBrasil.init();
    portalBrasilCompor.init();
});
