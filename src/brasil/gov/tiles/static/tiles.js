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


(function($) {
    function AudioPlayer(audio_element, conf) {
        var self = this,
            cssSelectorAncestor = conf.cssSelectorAncestor,
            ae = audio_element;

        $.extend(self, {
            init: function(){
                var audio_url = self.get_audio_url();
                var media = self.get_media(audio_url);

                ae.jPlayer({
                    ready: function () {
                        $(this).jPlayer("setMedia", media.media_urls);
                    },
                    swfPath: "/++resource++brasil.gov.tiles",
                    supplied: 'mp3,m4a,oga,webma',
                    cssSelectorAncestor: cssSelectorAncestor,
                    solution:"html,flash",
                    wmode: "window"
                });
            },

            /**
             * Construct the setMedia list of option and the supplied list
             * XXX at this point is not really used because a bug in the player
             **/
            get_media: function(urls){
                //right now works for only 1 media type but should be modify 
                //to iterate over urls and provide multiple supplied and sources
                var media = {'media_urls':{}, 'supplied':''};
                var media_type = self.get_media_type(urls);

                if (media_type){
                    media['media_urls'][media_type] = urls;
                    media['supplied'] = media_type;
                }
                return media;
            },

            /**
             * Get the audio url from the configuration or the data attribute in the
             * main element
             **/
            get_audio_url: function(){
                var url = conf.audio_url? conf.audio_url : ae.data('audio-url');
                return url;
            },

            /**
             * Function to gleam the media type from the URL
             * 
             **/
            get_media_type: function(url) { 
                var mediaType = false;
                if(/\.mp3$/i.test(url)) {
                    mediaType = 'mp3';
                } else if(/\.mp4$/i.test(url) || /\.m4v$/i.test(url)) {
                    mediaType = 'm4v';
                } else if(/\.m4a$/i.test(url)) {
                    mediaType = 'm4a';
                } else if(/\.ogg$/i.test(url) || /\.oga$/i.test(url)) {
                    mediaType = 'oga';
                } else if(/\.ogv$/i.test(url)) {
                    mediaType = 'ogv';
                } else if(/\.webm$/i.test(url)) {
                    mediaType = 'webmv';
                }
                return mediaType;
            },

            /**
             * Method to update the media element reproduced in the player
             * requires just a media url
             **/
            update_player: function(new_url) {
                //clear all media (even if is running)
                //ae.jPlayer("clearMedia");
                conf.audio_url = new_url;

                var audio_url = self.get_audio_url();
                var media = self.get_media(audio_url);

                ae.jPlayer( "clearMedia" );
                ae.jPlayer("option", 'swfPath', '/++resource++brasil.gov.tiles');

                ae.jPlayer("option", "supplied", media.supplied);
                ae.jPlayer("setMedia", media.media_urls);

            }
        });
        self.init();
    }

    $.fn.audio_player = function(options) {

        // already instanced, return the data object
        var el = this.data("audio_player");
        if (el) { return el; }


        var default_settings = this.data('audio_player-settings');
        var settings = '';
        //default settings
        if (default_settings) {
            settings = default_settings;
        } else {
            settings = {
                'cssSelectorAncestor': '#jp_container_1',
            }
        }

        if (options) {
            $.extend(settings, options);
        }

        return this.each(function() {
            el = new AudioPlayer($(this), settings);
            $(this).data("audio_player", el);
        });

    };
})(jQuery);

(function($) {

    function AudioGallery(gallery) {
        var self = this,
            gallery_obj = gallery,
            player = gallery_obj.find('.jp-jplayer'),
            ancestor = '#' + gallery_obj.find('.jp-audio').attr('id');

        $.extend(self, {
            init: function(){
                self.bind_events();
                player.audio_player({'cssSelectorAncestor':ancestor});
            },

            bind_events: function() {
                var links = gallery_obj.find('.audiogallery-item');
                links.click(function(e){
                    e.preventDefault();
                    self.update($(this).attr('href'));
                    links.parent('li').removeClass('selected');
                    $(this).parent('li').addClass('selected');
                    gallery_obj.find('.audiogallery-item-title').html($(this).html());
                });
            },

            update: function(url) {
                var p = player.audio_player({'cssSelectorAncestor':ancestor});
                p.update_player(url);
            }
        });
        self.init();
    }

    $.fn.audiogallery = function() {

        // already instanced, return the data object
        var el = this.data("audiogallery");
        if (el) { return el; }


        var default_settings = this.data('audiogallery-settings');

        return this.each(function() {
            el = new AudioGallery($(this));
            $(this).data("audiogallery", el);
        });

    };
})(jQuery);


(function($) {

    function MediaCarousel(mediacarousel) {
        var self = this,
            galleria_id = mediacarousel.attr('id');

        $.extend(self, {
            init: function(){
                self.setup_size();

                Galleria.loadTheme('++resource++brasil.gov.tiles/galleria.classic.min.js');
                Galleria.run('#' + galleria_id);
            },

            setup_size: function() {
                //proportions is going to be 4/3, requeriment defined.
                var width = mediacarousel.width();
                mediacarousel.height(width/1.33333);
            }
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
})(jQuery);