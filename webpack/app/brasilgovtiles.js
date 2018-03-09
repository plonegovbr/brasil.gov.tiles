import Albuns from './js/tiles/albuns.js';
import AudioGallery from './js/tiles/audiogallery.js';
import { BannerRotativo, BannerRotativoCompor } from './js/tiles/banner_rotativo.js';
import CarouselResponsiveResize from './js/tiles/mediacarousel.js';
import VideoResponsiveResize from './js/tiles/videogallery.js';


$(() => {
  if ($('.mediacarousel-tile')[0] !== undefined) {
    let resize = function () {
      let carouselResponsiveResize = new CarouselResponsiveResize();
      carouselResponsiveResize.resize();
    }
    $(window).resize(function () {
      resize();
    });
    resize();
  }
  if ($('.videogallery-tile')[0] !== undefined) {
    let resize = function () {
      let videoResponsiveResize = new VideoResponsiveResize();
      videoResponsiveResize.resize();
    }
    $(window).resize(function () {
      resize();
    });
    resize();
  }
});


$(window).load(() => {
  if ($('#tile_banner_rotativo').length > 0) {
    BannerRotativo.init();
    BannerRotativoCompor.init();
    BannerRotativo.resizeAlturaBannerRotativo();
  }
  Albuns.carrossel();
});


export default {
  Albuns,
  AudioGallery,
  BannerRotativo,
  BannerRotativoCompor,
  CarouselResponsiveResize,
  VideoResponsiveResize,
}
