export default class GalleryTile {
  constructor(tile) {
    this.tile = tile;
    this.initSwiper();
    this.composeMode();
  }
  initSwiper() {
    this.galleryTop = new Swiper(`#${this.tile.id} .gallery-top`, {
      grabCursor: true
    });
    this.galleryThumbs = new Swiper(`#${this.tile.id} .gallery-thumbs`, {
      virtualTranslate: true,
      navigation: {
        nextEl: `#${this.tile.id} .gallery-thumbs-container .swiper-button-next`,
        prevEl: `#${this.tile.id} .gallery-thumbs-container .swiper-button-prev`,
      },
      centeredSlides: true,
      slidesPerView: 'auto',
      touchRatio: 0.2,
      slideToClickedSlide: true,
    });
    this.galleryThumbs.on('slideChange', this.slideChange);
    this.galleryTop.controller.control = this.galleryThumbs;
    this.galleryThumbs.controller.control = this.galleryTop;
  }
  composeMode() {
    if ($('.template-compose').length === 0) {
      return;
    }
    $(`#${this.tile.id} .gallery-thumbs`).prepend(
      '<div class="crop-warning">Recorte a imagem na opção "mini" para corrigir as miniaturas.</div>'
    );
    for (let thumbnail of $(`#${this.tile.id} .gallery-thumbs .swiper-slide`)) {
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
