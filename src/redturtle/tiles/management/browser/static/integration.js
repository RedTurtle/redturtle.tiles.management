require([
  'jquery',
  'mockup-patterns-sortable',
  'mockup-patterns-modal',
], function($, Sortable, Modal) {
  'use strict';
   $(document).ready(function(){
      //add tile button
      $('.add-tile-btn').each(function() {
        var add_modal = new Modal($(this), {
          buttons: '.formControls input[type="submit"]#buttons-save, .formControls input[type="submit"]#buttons-cancel',
          templateOptions: {
            classModal: 'plone-modal-content add-tile-modal',
          },
          handleLinkAction: function($action, options, patternOptions) {
            window.location.href = $action.attr('href');
          }
        });
      });
    
      //edit buttons
      var tiles = $('.tilesList').attr('data-jsontiles');
      if (!tiles) {
        //the user can't manage tiles
        return;
      }
      var absolute_url = $("body").data().baseUrl;
      var tiles_obj = JSON.parse(tiles);
    
      tiles_obj.forEach(function(tile_obj) {
        var tile_wrapper = $('[data-tileid=' + tile_obj.tile_id + ']');
        if (tile_wrapper === undefined) {
          return;
        }
        var edit_url = absolute_url + '/@@edit-tile/' + tile_obj.tile_type + '/' + tile_obj.tile_id;
        var delete_url = absolute_url + '/@@delete-tile/' + tile_obj.tile_type + '/' + tile_obj.tile_id;
        var html = '<div class="tileEditButtons">';
          html += '<a class="plone-btn plone-btn-info tileEditLink" href="' + edit_url + '">';
          html += '<span class="icon-edit" aria-hidden="true"></span>';
          html += '</a>';
          html += '<a class="pat-plone-modal plone-btn plone-btn-danger tileDeleteLink" href="' + delete_url + '">';
          html += '<span class="icon-delete" aria-hidden="true">X</span>';
          html += '</a>';
        $(html).hide().prependTo($(tile_wrapper));
        $('.tileDeleteLink').each(function() {
          var delete_modal = new Modal($(this), {
            templateOptions: {
              classModal: 'plone-modal-content delete-tile-modal',
            },
            actionOptions: {
              redirectOnResponse: false,
              onSuccess: function(self, response, state, xhr, form) {
                if (state === "success") {
                  self.hide();
                  self.reloadWindow();
                }
              }
            }
          });
        });
        $(tile_wrapper).mouseenter(function() {
          $(this).addClass('editableTile');
          $( this ).find( ".tileEditButtons" ).show();
        }).mouseleave(function() {
          $(this).removeClass('editableTile');
          $( this ).find( ".tileEditButtons" ).hide();
        });
      });
      //sortable tiles
      var sortable = new Sortable($('.tilesWrapper'), {
        selector: 'div.tileWrapper',
        drop: function($el, delta) {
          if (delta !== 0){
            var tile_ids = $('.tileWrapper').map(function(index, obj) {
              return $(obj).data().tileid;
            });
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
});
