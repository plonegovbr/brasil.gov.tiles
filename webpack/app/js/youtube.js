export default class Youtube {
  constructor() {
    this.$video = $('.swiper-video a, .tile-video a, .section-videos .tileItem a');
    this.$video.on('click', this.openVideo.bind(this));
    $(window).resize(this.resize.bind(this));
  }
  extractId(url) {
    let parser = document.createElement('a');
    parser.href = url;
    if (parser.href.indexOf('embed') >= 0) {
      return parser.pathname.split('/')[2];
    } else {
      return parser.search.split('=')[1];
    }
  }

  openVideo(e) {
    e.preventDefault();

    let url = e.target.dataset['url'];
    let videoId = '';
    let parser = document.createElement('a');
    parser.href = url;
    // check if link points to embedder
    if (parser.hostname === location.hostname) {
      $.ajax({
        headers: {
          Accept: 'application/json'
        },
        url: url,
        context: this
      }).done(function(data) {
        this.insertVideo(this.extractId(data.url));
      });
    } else {
      this.insertVideo(this.extractId(url));
    }
  }
  insertVideo(videoId) {
    $('body').append(
      `<div class="video-player">
         <iframe src="${location.protocol}//www.youtube.com/embed/${videoId}?rel=0&controls=0&showinfo=0&autoplay=1">
         </iframe>
       </div>`
    );
    $('.video-player').on('click', this.closeVideo.bind(this));
    this.$iframe = $('.video-player iframe');
    this.resize();
  }
  closeVideo(e) {
    e.preventDefault();
    $('.video-player').remove();
  }
  resize(e) {
    if (typeof(e) !== 'undefined') {
      e.preventDefault();
    }
    this.$iframe.height(this.$iframe.width() * 9 / 16);
  }
}

// WEBPACK FOOTER //
// ./app/js/youtube.js