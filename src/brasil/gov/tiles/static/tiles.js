/*
  Comentario
*/
$(document).ready(function() {
    //video gallery
    if ($('.videogallery-tile')[0] !== undefined) {
        var videoResponsiveResize, root;

        root = typeof exports !== "undefined" && exports !== null ? exports : this;

        root.VideoResponsiveResize = function () {
            var _Singleton, _base;
            _Singleton = (function () {
                function _Singleton() {}

                _Singleton.prototype.qtd_coluna_anterior = '';
                _Singleton.prototype.scrollbar = false;

                _Singleton.prototype.resize = function () {
                    var qtd_coluna_atual;

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

                        $('.videogallery-tile').each(function(){
                            $(this).removeClass('gallery-2-columns');
                            $(this).removeClass('gallery-3-columns');

                            if (qtd_coluna_atual === 2) {
                                $(this).addClass('gallery-2-columns');
                            } else if (qtd_coluna_atual === 3) { // Desktop
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
                };

                return _Singleton;
            })();


            if ((_base = root.VideoResponsiveResize).instance == null) {
                _base.instance = new _Singleton();
            }
            return root.VideoResponsiveResize.instance;
        };

        var resize = function () {
            videoResponsiveResize = new root.VideoResponsiveResize();
            videoResponsiveResize.resize();
        }

        $(window).resize(function () {
            resize();
        });

        resize();
    }

    if ($('.mediacarousel-tile')[0] !== undefined) {
        var carouselResponsiveResize, root;

        root = typeof exports !== "undefined" && exports !== null ? exports : this;

        root.CarouselResponsiveResize = function () {
            var _Singleton, _base;
            _Singleton = (function () {
                function _Singleton() {}

                _Singleton.prototype.qtd_coluna_anterior = '';
                _Singleton.prototype.scrollbar = false;

                _Singleton.prototype.resize = function () {
                    var qtd_coluna_atual;

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
                        var _i, _len;
                        var gallerias = Galleria.get();

                        for (_i = 0, _len = gallerias.length; _i < _len; _i++) {
                            var g = gallerias[_i];
                            if (g) {
                                var mediacarousel = '#' + g._target.id;
                                g.resize({
                                    width: g._stageWidth,
                                    height: g._stageWidth*3/4
                                });
                                $(mediacarousel).css({
                                    height: g._stageWidth*3/4
                                });

                                var bottomThumbs = $('.galleria-thumbnails-container', mediacarousel).offset().top +
                                    $('.galleria-thumbnails-container', mediacarousel).height();
                                var bottomContainer = $(mediacarousel).offset().top +
                                    $(mediacarousel).height();
                                var heightContainer = $(mediacarousel).height() +
                                    (bottomThumbs             -
                                     bottomContainer)         +
                                    ($(mediacarousel+' + .mediacarousel-footer-container a').text === '' ? 39: 18) +
                                    8;
                                $(mediacarousel).css({
                                    height: heightContainer
                                });
                            }
                        }
                    }
                };

                return _Singleton;
            })();


            if ((_base = root.CarouselResponsiveResize).instance == null) {
                _base.instance = new _Singleton();
            }
            return root.CarouselResponsiveResize.instance;
        };

        var resize = function () {
            carouselResponsiveResize = new root.CarouselResponsiveResize();
            carouselResponsiveResize.resize();
        }

        $(window).resize(function () {
            resize();
        });

        resize();
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
                    supplied: media.supplied,
                    cssSelectorAncestor: cssSelectorAncestor,
                    solution:"html,flash",
                    wmode: "window",
                    preload: "none"
                });
            },

            /**
             * Construct the setMedia list of option and the supplied list
             **/
            get_media: function(urls){
                var media = {'media_urls':{}, 'supplied':''};
                var media_type, url, _i, _len;

                urls = urls.split(';');
                for (_i = 0, _len = urls.length; _i < _len; _i++) {
                    url = urls[_i];
                    media_type = self.get_media_type(url);
                    if (media_type){
                        media['media_urls'][media_type] = url;
                        if (media['supplied']) {
                            media['supplied'] += ', ';
                        }
                        media['supplied'] += media_type;

                    }
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
                Galleria.loadTheme('++resource++brasil.gov.tiles/galleria.classic.min.js');

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


                    if (!$(mediacarousel).hasClass('image')){
                        $(mediacarousel).addClass('image');

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
                        $(mediacarousel).animate({
                            height: heightContainer
                        });
                        $('.galleria-thumbnails-container, .galleria-info').animate({
                            opacity: 1
                        });
                    }
                });

                Galleria.run('#'+galleria_id);

                Galleria.ready(function() {
                    var galleriaContainer = $('#'+this._target.id);
                    if (!galleriaContainer.hasClass('ready')) {
                        galleriaContainer.addClass('ready');
                        var galleriaContainerWidth  = galleriaContainer.width(),
                            galleriaContainerHeight = (galleriaContainerWidth*3)/4;
                        this.resize({
                            width: galleriaContainerWidth,
                            height: galleriaContainerHeight
                        });
                    }
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
})(jQuery);
