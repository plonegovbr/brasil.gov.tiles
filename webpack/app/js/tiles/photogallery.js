import Swiper from 'swiper';


export default class PhotoGalleryTile {
    constructor(tile) {
      this.tile = tile;
      this.initSwiper();
    }
    initSwiper() {
      this.galleryThumbs = new Swiper(`#${this.tile.id} .photogallery-container`, {
        navigation: {
          nextEl: `#${this.tile.id} .photogallery-container .swiper-button-next`,
          prevEl: `#${this.tile.id} .photogallery-container .swiper-button-prev`,
        },
      });
    }
  }
