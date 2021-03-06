import Albuns from './js/tiles/albuns.js';
import AudioGallery from './js/tiles/audiogallery.js';
import GroupCarouselTile from './js/tiles/groupcarousel.js';
import HighlightsCarouselTile from './js/tiles/highlightscarousel.js';
import NavigationTile from './js/tiles/navigation.js';
import PhotoGalleryTile from './js/tiles/photogallery.js';
import POTDTile from './js/tiles/potd.js';
import TileShare from './js/tileshare.js';
import VideoCarouselTile from './js/tiles/videocarousel.js';
import VideoResponsiveResize from './js/tiles/videogallery.js';


// https://hacks.mozilla.org/2015/04/es6-in-depth-iterators-and-the-for-of-loop/
jQuery.prototype[Symbol.iterator] = Array.prototype[Symbol.iterator];


$(() => {
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
  for (let videocarousel of $('.brasil-videocarousel-tile')) {
    new VideoCarouselTile(videocarousel);
  }
  for (let carousel of $('.brasil-groupcarousel-tile')) {
    new GroupCarouselTile(carousel);
  }
  for (let carousel of $('.brasil-highlightscarousel-tile')) {
    new HighlightsCarouselTile(carousel);
  }
  if ($('.portaltype-collective-cover-content').length > 0) {
    for (let tile of $('.box-colorido .cover-richtext-tile, .nitf-basic-tile')) {
      new TileShare(tile);
    }
  }
});


$(window).load(() => {
  Albuns.carrossel();
});


export default {
  Albuns,
  AudioGallery,
  VideoResponsiveResize,
  POTDTile,
  PhotoGalleryTile,
  NavigationTile,
  GroupCarouselTile,
  HighlightsCarouselTile,
}
