export default class NavigationTile {
  constructor(tile) {
    this.tile = tile;
    this.$('.navigation-more').on('click', this.moreClick.bind(this));
  }
  $(selector) {
    return $(selector, this.tile);
  }
  moreClick(e) {
    e.preventDefault();
    this.$('.navigation-more').toggleClass('open');
    this.$('.navigation-more-items').toggleClass('open');
  }
}

