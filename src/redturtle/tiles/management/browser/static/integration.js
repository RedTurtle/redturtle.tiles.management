define([
  'jquery',
  'mockup-patterns-base',
  'mockup-patterns-sortable',
  'mockup-patterns-modal',
], function ($, Base, Sortable, Modal) {
  'use strict';
  var Pattern = Base.extend({
    name: 'tiles-management',
    trigger: '.pat-tiles-management',
    parser: 'mockup',
    defaults: {
    },
    init: function () {
      const _this = this;
      const managerId = this.options.managerId;

      const initializeAddButton = function (button, url) {
        const $button = $(button);
        var container = $button.next('.available-tiles');
        if (container.length === 0) {
          $button.parent().append('<div class="available-tiles"></div>');
          container = $button.next('.available-tiles');
          container.hide();
          container.load(url + ' #content .list-group', function () {
            container.find('a.list-group-item').each(function () {
              const addTileModal = new Modal($(this), {
                actionOptions: {
                  redirectOnResponse: true,
                },
              });
              addTileModal.on('after-render', function () {
                $('form#add_tile').append('<input type="hidden" name="managerId" value="' + managerId + '" />');
              });
            });

            $(this).slideDown();
          });
        } else {
          container.slideToggle();
        }
      };

      const enableEditButtons = function (tile) {
        //edit buttons modals
        const $tile = $(tile);
        $tile.find('div.tileEditButtons a.tileDeleteLink').each(function () {
          const deleteModal = new Modal($(this), {
            templateOptions: {
              classModal: 'plone-modal-content delete-tile-modal',
            },
            actionOptions: {
              redirectOnResponse: false,
              onSuccess: function (self, response, state, xhr, form) {
                if (state === 'success') {
                  self.hide();
                  self.reloadWindow();
                }
              },
            },
          });
          deleteModal.on('after-render', function () {
            $('form#delete_tile').append('<input type="hidden" name="managerId" value="' + managerId + '" />');
          });
        });

        $tile.find('div.tileEditButtons a.tileEditLink').each(function () {
          const editModal = new Modal($(this), {
            templateOptions: {
              classModal: 'plone-modal-content edit-tile-modal',
            },
            actionOptions: {
              redirectOnResponse: true,
            },
          });
        });

        $tile.find('div.tileEditButtons a.tileVisibilityLink').each(function () {
          $(this).click(function (e) {
            e.preventDefault();
            $.get(e.currentTarget.href + '&managerId=' + managerId)
              .done(function (data) {
                if (data !== undefined) {
                  const result = JSON.parse(data);
                  console.error(result.error);
                  return;
                }

                const contentlUrl = $('body').data('baseUrl');
                const tilesInfosUrl = contentlUrl + '/tiles_management?managerId=' + managerId + '&ajax_load=true .tilesWrapper';
                $.get(tilesInfosUrl)
                  .done(function (data) {
                    const tileId = $tile.data('tileid');
                    const html = $('<div></div>').html(data);
                    const newTile = html.find('.tilesList .tileWrapper[data-tileid="' + tileId + '"]');
                    $tile.replaceWith(newTile);
                    enableEditButtons(newTile);
                    enableSorting(newTile.parent());
                  });
              })
              .fail(function (error) {
                console.error(error);
              });
          });
        });

        $tile.mouseenter(function () {
          $(this).addClass('editableTile');
          $(this).find('.tileEditButtons').show();
        }).mouseleave(function () {
          $(this).removeClass('editableTile');
          $(this).find('.tileEditButtons').hide();
        });
      };

      const enableSorting = function (container) {
        const absoluteUrl = $('body').data().baseUrl || $('base').attr('href');
        const sortable = new Sortable(container.find('.tilesList'), {
          selector: 'div.tileWrapper',
          drop: function ($el, delta) {
            if (delta !== 0) {
              const tileIds = $('.tileWrapper').map(function (index, obj) {
                return $(obj).data().tileid;
              });

              if (absoluteUrl !== undefined) {
                $.get(
                  absoluteUrl + '/reorder_tiles',
                  {
                    tileIds: JSON.stringify(tileIds.get()),
                    managerId: managerId,
                  })
                  .done(function (data) {
                    if (data !== '') {
                      const result = JSON.parse(data);
                      console.error(result.message);
                    }
                  })
                  .fail(function (error) {
                    console.error(error);
                  });
              }
            }
          },
        });
      };

      const loadManager = function (container) {
        const contentlUrl = $('body').data('baseUrl');
        const tilesInfosUrl = contentlUrl + '/tiles_management?managerId=' + managerId + '&ajax_load=true .tilesWrapper';
        container.load(tilesInfosUrl, function () {
          const addButton = container.find('.add-tile-btn');
          if (addButton.length > 0) {
            container.find('.tilesList .tileWrapper').each(function () {
              container.find('.tileEditButtons').hide();
              enableEditButtons(this);
            });

            enableSorting(container);
            addButton.each(function () {
              $(this).click(function (e) {
                e.preventDefault();
                initializeAddButton($(this), e.target.href);
              });
            });
          }
        });

      };

      if (!managerId) {
        _this.$el.append('<span>to use tiles manager, you need to provide a managerId attribute</span>');
      } else {
        loadManager(_this.$el);
      }

    },
  });
  return Pattern;
});
