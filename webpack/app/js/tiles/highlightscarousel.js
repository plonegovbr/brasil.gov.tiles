import Swiper from 'swiper/dist/js/swiper.js';


export default class HighlightsCarouselTile {
  constructor(tile) {
    this.tile = tile;
    this.initSwiper();
    this.composeMode();
  }
  initSwiper() {
    this.carouselTop = new Swiper(`#${this.tile.id} .carousel-top`, {
      grabCursor: true
    });
    this.carouselThumbs = new Swiper(`#${this.tile.id} .carousel-thumbs`, {
      virtualTranslate: true,
      navigation: {
        nextEl: `#${this.tile.id} .carousel-thumbs-container .swiper-button-next`,
        prevEl: `#${this.tile.id} .carousel-thumbs-container .swiper-button-prev`,
      },
      centeredSlides: true,
      slidesPerView: 'auto',
      touchRatio: 0.2,
      slideToClickedSlide: true,
    });
    this.carouselThumbs.on('slideChange', this.slideChange);
    this.carouselTop.controller.control = this.carouselThumbs;
    this.carouselThumbs.controller.control = this.carouselTop;
  }
  composeMode() {
    if ($('.template-compose').length === 0) {
      return;
    }
    $(`#${this.tile.id} .carousel-thumbs`).prepend(
      '<div class="crop-warning">Recorte a imagem na opção "mini" para corrigir as miniaturas.</div>'
    );
    for (let thumbnail of $(`#${this.tile.id} .carousel-thumbs .swiper-slide`)) {
      let $thumbnail = $(thumbnail);
      let $img = $('img', $thumbnail);
      let parser = document.createElement('a');
      parser.href = $img.attr('src');
      parser.pathname = parser.pathname.replace(/\@\@.*/, '@@croppingeditor');
      parser.search = 'scalename=mini';
      $thumbnail.append(`<a class="crop" target="_blank" href="${parser.href}" title="Recortar imagem">✀</span>`);
    }
  }
  slideChange() {
    let thumbsLeft = this.$el.offset().left -5;
    let thumbsRight = thumbsLeft + this.$el.outerWidth() + 10;

    let $currentSlide = $(this.slides[this.activeIndex]);
    let currentSlideLeft = $currentSlide.offset().left;
    let currentSlideRight = currentSlideLeft + $currentSlide.outerWidth();

    if (currentSlideLeft < thumbsLeft || currentSlideRight > thumbsRight) {
      let wrapperLeft = this.$wrapperEl.offset().left;
      this.$wrapperEl.transform(`translate(${thumbsLeft - currentSlideLeft + wrapperLeft}px)`);
    }
  }
}
