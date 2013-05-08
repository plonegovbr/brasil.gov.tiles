/* 
  Comentario
*/
$(document).ready(function() {
    //video gallery
    if ($('.videogallery-tile')[0] !== undefined) {
        $('.videogallery-tile').each(function(){


            //fake responsive (1, 2 or 3 columns)
            var width = $(this).width();
            // 2 column, 230
            if (width > 280) {
                $(this).addClass('gallery-2-columns');
            }
            // 3 columns, 460 + 30 padding
            if (width > 500) {
                $(this).removeClass('gallery-2-columns');
                $(this).addClass('gallery-3-columns');
            }

            //resize video onload
            var video_width = $('.player-holder iframe').width();
            $('.player-holder iframe').height(video_width/1.3333);

            //video loading logic
            var video_gallery = $(this);
            var gallery_link = video_gallery.find('.gallery-element').find('.gallery-element-link');
            gallery_link.click(function(e){
                e.preventDefault();

                var player = $(this).data('player-dom');
                var metadata = $(this).siblings('.gallery-element-metadata');

                video_gallery.find('.selected').removeClass('selected');
                $(this).parents('.gallery-element').addClass('selected');
                
                var player_slot = video_gallery.find('.player-holder');
                player_slot.find('.player-video').html(player);
                player_slot.find('.title').html(metadata.find('.title').html());
                player_slot.find('.description').html(metadata.find('.description').html());

                //resize video onload
                var video_width = $('.player-holder iframe').width();
                $('.player-holder iframe').height(video_width/1.3333);

            });
        });
    }
});