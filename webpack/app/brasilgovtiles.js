import Albuns from './js/tiles/albuns.js';
import AudioGallery from './js/tiles/audiogallery.js';
import { BannerRotativo, BannerRotativoCompor } from './js/tiles/banner_rotativo.js';
import CarouselResponsiveResize from './js/tiles/mediacarousel.js';
import VideoResponsiveResize from './js/tiles/videogallery.js';
import POTDTile from './js/tiles/potd.js';
import PhotoGalleryTile from './js/tiles/photogallery.js';
import CarouselTile from './js/tiles/carousel.js';
import GalleryTile from './js/tiles/gallery.js';
import NavigationTile from './js/tiles/navigation.js';

// https://hacks.mozilla.org/2015/04/es6-in-depth-iterators-and-the-for-of-loop/
jQuery.prototype[Symbol.iterator] = Array.prototype[Symbol.iterator];

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
  for (let tile of $('.potd-tile')) {
    new POTDTile();
  }
  for (let tile of $('.brasil-photogallery-tile')) {
    new POTDTile();
    new PhotoGalleryTile(tile);
  }
  for (let navigation of $('.brasil-navigation-tile')) {
    new NavigationTile(navigation);
  }
  for (let gallery of $('.brasil-gallery-tile')) {
    new GalleryTile(gallery);
  }
  $('#viewlet-social-like').stop(true, true);
  for (let carousel of $('.brasil-carousel-tile')) {
    new CarouselTile(carousel);
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
  POTDTile,
  PhotoGalleryTile,
  NavigationTile,
  GalleryTile,
  CarouselTile,
}

