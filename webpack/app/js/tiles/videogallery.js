let instance = null;


let VideoResponsiveResize = function () {
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

        $('.videogallery-tile').each(function(){
          $(this).removeClass('gallery-2-columns');
          $(this).removeClass('gallery-3-columns');

          if (qtd_coluna_atual === 2) {
            $(this).addClass('gallery-2-columns');
          } else if (qtd_coluna_atual === 3) { // Desktop
            $(this).addClass('gallery-3-columns');
          }

          //resize video onload
          let video_width = $('.player-holder iframe').width();
          $('.player-holder iframe').height(video_width/1.3333);

          //video loading logic
          let video_gallery = $(this);
          let gallery_link = video_gallery.find('.gallery-element').find('.gallery-element-link');
          gallery_link.click(function(e){
            e.preventDefault();

            let player = $(this).data('player-dom');
            let metadata = $(this).siblings('.gallery-element-metadata');

            video_gallery.find('.selected').removeClass('selected');
            $(this).parents('.gallery-element').addClass('selected');

            let player_slot = video_gallery.find('.player-holder');
            player_slot.find('.player-video').html(player);
            player_slot.find('.title').html(metadata.find('.title').html());
            player_slot.find('.description').html(metadata.find('.description').html());

            //resize video onload
            let video_width = $('.player-holder iframe').width();
            $('.player-holder iframe').height(video_width/1.3333);
          });
        });
      }
    };

    return _Singleton;
  })();

  if (instance == null) {
    instance = new _Singleton();
  }
  return instance;
};


export default VideoResponsiveResize;
