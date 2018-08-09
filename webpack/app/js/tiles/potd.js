export default class POTDTile {
    constructor() {
  
        this.img = $('.zoom-icon');
        this.img.on('click', this.openImage.bind(this.img));
    }
    openImage(e){
        e.preventDefault();
        let url = e.target.href;
        if ($('#image-overlay').length === 0) {
          $('body').append(
              `<div id="image-overlay" class="overlay overlay-ajax">
                  <div class="pb-image"><img src="${url}"/></div>
              </div>`);
        }
        $('#image-overlay').show();
        $('#image-overlay').on('click', function(){$('#image-overlay').remove()});
    }
  }