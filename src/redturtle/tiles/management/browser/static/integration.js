require([
  'jquery',
  'mockup-patterns-sortable',
], function($, Sortable) {
  'use strict';
  //edit buttons
  $('.tileWrapper').each(function() {
    var edit_url = $(this).attr('data-editurl');
    var delete_url = $(this).attr('data-deleteurl');
    if ((edit_url === undefined) && (delete_url === undefined)) {
      return;
    }
    var html = '<div class="tileEditButtons">';
    if (edit_url) {
      html += '<a class="plone-btn plone-btn-primary tileEditLink" href="' + edit_url + '">';
      html += '<span class="icon-edit" aria-hidden="true"></span>';
      html += '</a>';
    }
    if (delete_url) {
      html += '<a class="plone-btn plone-btn-danger tileEditLink" href="' + delete_url + '">';
      html += '<span class="icon-delete" aria-hidden="true">X</span>';
      html += '</a>';
    }
    $(html).hide().prependTo($(this));
  });
  $('.tileWrapper').mouseenter(function() {
    $(this).addClass('editableTile');
    $( this ).find( ".tileEditButtons" ).show();
  }).mouseleave(function() {
    $(this).removeClass('editableTile');
    $( this ).find( ".tileEditButtons" ).hide();
  });

  //sortable tiles
  var sortable = new Sortable($('.tilesWrapper'), {
    selector: 'div.tileWrapper',
    drop: function($el, delta) {
      if (delta !== 0){
        var tile_ids = $('.tileWrapper').map(function(index, obj) {
          return $(obj).data().tileid;
        });
        var absolute_url = $("body").data().baseUrl;
        if (absolute_url !== undefined) {
          $.get( absolute_url + "/reorder_tiles", {tile_ids: JSON.stringify(tile_ids.get())})
            .done(function(data) {
              if (data !== "") {
                result = JSON.parse(data);
                console.error(data.message);
              }
            })
            .fail(function(error) {
              console.error(error);
            });
        }
      }
    }
  });
});
