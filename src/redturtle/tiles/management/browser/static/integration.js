define('tiles-management-pattern', [
  'jquery',
  'pat-base',
  'pat-registry',
  'mockup-patterns-modal',
  'mockup-patterns-sortable',
  'mockup-i18n',
  'babel-polyfill',
], function ($, Base, registry, Modal, Sortable, I18n) {
  'use strict';
  var Pattern = Base.extend({
    name: 'tiles-management',
    trigger: '.pat-tiles-management',
    parser: 'mockup',
    defaults: {},
    init: function () {
      const _this = this;
      const managerId = this.options.managerId;

      const isIE = (function () {
        var ua = window.navigator.userAgent;
        var msie = ua.indexOf('MSIE ');
        if (msie > 0) {
          // IE 10 or older => return version number
          return true;
        }

        var trident = ua.indexOf('Trident/');
        if (trident > 0) {
          // IE 11 => return version number
          return true;
        }

        var edge = ua.indexOf('Edge/');
        if (edge > 0) {
          // IE 12 (aka Edge) => return version number
          return true;
        }

        // other browser
        return false;
      })();

      const customEventPolyfill = function () {
        if (typeof window.CustomEvent === 'function') return false;

        function CustomEvent(event, params) {
          params = params || {
            bubbles: false,
            cancelable: false,
            detail: undefined,
          };
          var evt = document.createEvent('CustomEvent');
          evt.initCustomEvent(
            event,
            params.bubbles,
            params.cancelable,
            params.detail,
          );
          return evt;
        }

        CustomEvent.prototype = window.Event.prototype;

        window.CustomEvent = CustomEvent;
      };

      customEventPolyfill(); // for IE11 compatibility

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
                  timeout: 10000,
                  redirectToUrl: window.location.href,
                },
              });
              addTileModal.on('after-render', function () {
                $('form#add_tile').append(
                  '<input type="hidden" name="managerId" value="' +
                  managerId +
                  '" />',
                );
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
              timeout: 10000,
              onSuccess: function (self, response, state, xhr, form) {
                if (state === 'success') {
                  self.hide();
                  self.reloadWindow();
                }
              },
            },
          });
          deleteModal.on('after-render', function () {
            $('form#delete_tile').append(
              '<input type="hidden" name="managerId" value="' +
              managerId +
              '" />',
            );
          });
        });

        $tile.find('div.tileEditButtons a.tileEditLink').each(function () {
          const editModal = new Modal($(this), {
            templateOptions: {
              classModal: 'plone-modal-content edit-tile-modal',
            },
            actionOptions: {
              redirectOnResponse: true,
              timeout: 10000,
            },
          });
        });

        $tile
          .find(
            'div.tileEditButtons a.tileVisibilityLink, div.tileEditButtons .tileSizeLink a',
          )
          .each(function () {
            $(this).click(function (e) {
              e.preventDefault();
              let options = {
                managerId: managerId,
                ajax_load: true
              };
              if (isIE) {
                options.invalidIECache = new Date().getTime();
              }
              $.get(e.currentTarget.href, options)
                .done(function (data) {
                  if (data !== undefined) {
                    const result = JSON.parse(data);
                    console.error(result.error);
                    return;
                  }

                  const contentlUrl = $('body').data('baseUrl');
                  const tilesInfosUrl = contentlUrl + '/tiles_management';
                  let options = {
                    managerId: managerId,
                    ajax_load: true
                  };
                  if (isIE) {
                    options.invalidIECache = new Date().getTime();
                  }
                  $.get(tilesInfosUrl, options).done(function (data) {
                    const tileId = $tile.data('tileid');
                    const html = $('<div></div>').html(data);
                    const newTile = html.find(
                      '.tilesList .tileWrapper[data-tileid="' + tileId + '"]',
                    );
                    $tile.replaceWith(newTile);
                    enableEditButtons(newTile);
                    const container = newTile.parents('.tilesWrapper');
                    if (container.length === 1 && window.innerWidth > 991) {
                      enableSorting($(container[0]));
                    }
                  });
                })
                .fail(function (error) {
                  console.error(error);
                });
            });
          });

        $tile
          .mouseenter(function () {
            $(this).addClass('editableTile');
            $(this)
              .find('.tileEditButtons')
              .show();
          })
          .mouseleave(function () {
            $(this).removeClass('editableTile');
            $(this)
              .find('.tileEditButtons')
              .hide();
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
                let options = {
                  managerId: managerId,
                  ajax_load: true,
                  tileIds: JSON.stringify(tileIds.get()),
                  _authenticator: $el.data('token'),
                };
                if (isIE) {
                  options.invalidIECache = new Date().getTime();
                }
                $.get(absoluteUrl + '/reorder_tiles', options)
                  .done(function (data) {
                    if (data && data !== '') {
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

      const enablePatterns = function (container) {
        // we need to manually enable patterns of tiles loaded with ajax because
        // sometimes these are loaded after pattern inits
        const tags = container.find('[class*="pat-"]');
        if (tags.length === 0) {
          return;
        }

        tags.each(function () {
          const _this = this;
          this.className.split(' ').map(function (cssClass) {
            if (cssClass.indexOf('pat-') !== -1) {
              const pattern = cssClass.substring(4);
              try {
                registry.initPattern(pattern, _this, cssClass);
              } catch (e) {
                if (e instanceof TypeError) {
                  //pattern already registered
                  return;
                }
              }
            }
          });
        });
      };

      const addLoader = function (container) {
        const portalUrl = $('body').data('portalUrl');
        container.html(
          '<div class="loading-tiles"><img src="' +
          portalUrl +
          '/++resource++redturtle.tiles.management/loader.svg" alt="loading"/></div>',
        );
      };

      const loadManager = function (container) {
        const contentlUrl = $('body').data('baseUrl');
        const tilesInfosUrl = contentlUrl + '/tiles_management';
        addLoader(container);
        let options = {
          managerId: managerId,
          ajax_load: true
        };
        if (isIE) {
            options.invalidIECache = new Date().getTime();
        }
        if ($('body').hasClass('userrole-anonymous')){
            $.ajaxSetup({cache: true});
        }
        $.get(tilesInfosUrl, options)
          .done(function (data) {
            // All subsequent Ajax calls using any function will use the new settings, 
            // unless overridden by the individual calls, until the next invocation of $.ajaxSetup().
            $.ajaxSetup({cache: false});
            const html = $(data);
            if (!html.length) {
              container.remove();
              return;
            }
            container.html($(data));

            //throw custom event to notify when tiles are loaded
            var event = new CustomEvent('rtTilesLoaded');
            container[0].dispatchEvent(event);

            enablePatterns(container);

            const addButton = container.find('.add-tile-btn');
            if (addButton.length > 0) {
              container.find('.tilesList .tileWrapper').each(function () {
                container.find('.tileEditButtons').hide();
                enableEditButtons(this);
              });

              if (window.innerWidth > 991) {
                enableSorting(container);
              }

              addButton.each(function () {
                $(this).click(function (e) {
                  e.preventDefault();
                  initializeAddButton($(this), e.target.href);
                });
              });
            }
          })
          .fail(function (err) {
            // All subsequent Ajax calls using any function will use the new settings, 
            // unless overridden by the individual calls, until the next invocation of $.ajaxSetup().
            $.ajaxSetup({cache: false});
            console.trace(err);
            var i18n = new I18n();
            const domain = 'redturtle.tiles.management';
            i18n.loadCatalog(domain);
            var _ = i18n.MessageFactory(domain);
            container.html(
              '<p class="error-manager">' + _('error_loading_manager') + '</p>',
            );
          });
      };

      if (!managerId) {
        _this.$el.append(
          '<span>to use tiles manager, you need to provide a managerId attribute</span>',
        );
      } else {
        loadManager(_this.$el);
      }
    },
  });

  return Pattern;
});
