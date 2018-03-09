function AudioPlayer(audio_element, conf) {
  let self = this,
    cssSelectorAncestor = conf.cssSelectorAncestor,
    ae = audio_element;

  $.extend(self, {
    init: function(){
      let audio_url = self.get_audio_url();
      let media = self.get_media(audio_url);

      ae.jPlayer({
        ready: function () {
          $(this).jPlayer("setMedia", media.media_urls);
        },
        swfPath: "/++resource++brasil.gov.tiles/vendor",
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
      let media = {'media_urls':{}, 'supplied':''};
      let media_type, url, _i, _len;

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
      let url = conf.audio_url? conf.audio_url : ae.data('audio-url');
      return url;
    },

    /**
     * Function to gleam the media type from the URL
     *
     **/
    get_media_type: function(url) {
      let mediaType = false;
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

      let audio_url = self.get_audio_url();
      let media = self.get_media(audio_url);

      ae.jPlayer( "clearMedia" );
      ae.jPlayer("option", 'swfPath', '/++resource++brasil.gov.tiles/vendor');

      ae.jPlayer("option", "supplied", media.supplied);
      ae.jPlayer("setMedia", media.media_urls);

    }
  });
  self.init();
}

$.fn.audio_player = function(options) {

  // already instanced, return the data object
  let el = this.data("audio_player");
  if (el) { return el; }


  let default_settings = this.data('audio_player-settings');
  let settings = '';
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

function AudioGallery(gallery) {
  let self = this,
    gallery_obj = gallery,
    player = gallery_obj.find('.jp-jplayer'),
    ancestor = '#' + gallery_obj.find('.jp-audio').attr('id');

  $.extend(self, {
    init: function(){
      self.bind_events();
      player.audio_player({'cssSelectorAncestor':ancestor});
    },

    bind_events: function() {
      let links = gallery_obj.find('.audiogallery-item');
      links.click(function(e){
        e.preventDefault();
        self.update($(this).attr('href'));
        links.parent('li').removeClass('selected');
        $(this).parent('li').addClass('selected');
        gallery_obj.find('.audiogallery-item-title').html($(this).html());
      });
    },

    update: function(url) {
      let p = player.audio_player({'cssSelectorAncestor':ancestor});
      p.update_player(url);
    }
  });
  self.init();
}

$.fn.audiogallery = function() {
  // already instanced, return the data object
  let el = this.data("audiogallery");
  if (el) { return el; }


  let default_settings = this.data('audiogallery-settings');

  return this.each(function() {
    el = new AudioGallery($(this));
    $(this).data("audiogallery", el);
  });
};
