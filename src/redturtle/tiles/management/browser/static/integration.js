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
      var editable_tiles = $('.tilesList .tileWrapper .tileEditButtons');
      if (editable_tiles.length === 0) {
        //the user can't manage tiles
        return;
      }
      var absolute_url = $("body").data().baseUrl || $('base').attr('href');

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
      $('.tilesList .tileWrapper').each(function() {
        $(this).mouseenter(function() {
          $(this).addClass('editableTile');
          $( this ).find( ".tileEditButtons" ).show();
        }).mouseleave(function() {
          $(this).removeClass('editableTile');
          $( this ).find( ".tileEditButtons" ).hide();
        });
      });
      //sortable tiles
      var sortable = new Sortable($('.tilesList'), {
        selector: 'div.tileWrapper',
        drop: function($el, delta) {
          if (delta !== 0){
            var tile_ids = $('.tileWrapper').map(function(index, obj) {
              return $(obj).data().tileid;
            });
            if (absolute_url !== undefined) {
              $.get( absolute_url + "/reorder_tiles", {tile_ids: JSON.stringify(tile_ids.get())})
                .done(function(data) {
                  if (data !== "" && data !== undefined) {
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
