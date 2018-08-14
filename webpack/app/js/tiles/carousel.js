export default class CarouselTile {
  constructor(tile) {
    this.tile = tile;

    this.initSwiper();
    this.initSecondCarousel();
  }
  initSwiper() {
    this.swiper = new Swiper(`#${this.tile.id} .carousel-thumbs`, {
      navigation: {
        nextEl: `#${this.tile.id} .carousel-thumbs .swiper-button-next`,
        prevEl: `#${this.tile.id} .carousel-thumbs .swiper-button-prev`,
      },
      pagination: {
        el: `#${this.tile.id} .carousel-thumbs .swiper-pagination`,
        clickable: true,
      },
    });
  }
  initSecondCarousel() {
    let $column = $(this.tile).parents('.column');
    this.$tiles = $('.brasil-carousel-tile', $column);
    if (this.$tiles.length !== 2) {
      return;
    }
    this.$otherTile = this.$tiles.not(this.tile);
    this.hideSecondCarusel();
    this.initSwitCarousel();
  }
  hideSecondCarusel() {
    if ($('body.template-compose').length > 0) {
      return;
    }
    let $lastTile = this.$tiles.last();
    if (this.tile === $lastTile[0]) {
      $lastTile.hide();
    }
  }
  initSwitCarousel() {
    let $ul = $('<ul>');
    for (let tile of this.$tiles) {
      let text = $('.switch-carousel', tile).attr('data-text');
      if (typeof(text) === 'undefined') {
        return;
      }
      let $li = $(`<li>${text}</li>`)
      if (this.tile === tile) {
        $li.addClass('active');
      } else {
        $li.on('click', function(e) {
          e.preventDefault();
          $(this.tile).hide();
          this.$otherTile.show();
        }.bind(this));
      }
      $ul.append($li);
    }
    $('.switch-carousel', this.tile).append($ul);
  }
}
