module.exports = function(grunt) {
  'use strict';

  require('load-grunt-tasks')(grunt);
  var productRoot = 'src/redturtle/tiles/management/browser/static';
  grunt.initConfig({
    cssmin: {
      target: {
        files: {
          './src/redturtle/tiles/management/browser/static/tiles-management-compiled.css': [
            `${productRoot}/integration.css`
          ]
        }
      },
      options: {
        sourceMap: true
      }
    },
    requirejs: {
      'redturtle-tiles-management': {
        options: {
          baseUrl: './',
          generateSourceMaps: true,
          preserveLicenseComments: false,
          paths: {
            jquery: 'empty:',
            'pat-base': 'empty:',
            'pat-registry': 'empty:',
            'mockup-patterns-modal': 'empty:',
            'mockup-patterns-sortable': 'empty:',
            'mockup-i18n': 'empty:',
            'babel-polyfill': 'empty:',
            'tiles-management-pattern': `${productRoot}/integration`
          },
          wrapShim: true,
          name: `${productRoot}/bundle.js`,
          exclude: ['jquery'],
          out: `${productRoot}/tiles-management-compiled.js`,
          optimize: 'none'
        }
      }
    },
    babel: {
      options: {
        sourceMap: true,
        presets: ['es2015']
      },
      dist: {
        files: {
          './src/redturtle/tiles/management/browser/static/tiles-management-compiled.js':
            './src/redturtle/tiles/management/browser/static/tiles-management-compiled.js'
        }
      }
    },

    uglify: {
      'redturtle-tiles-management': {
        options: {
          sourceMap: true,
          sourceMapName: `./${productRoot}/redturtle-tiles-management-compiled.js.map`,
          sourceMapIncludeSources: false
        },
        files: {
          './src/redturtle/tiles/management/browser/static/tiles-management-compiled.js': [
            './src/redturtle/tiles/management/browser/static/tiles-management-compiled.js'
          ]
        }
      }
    },
    watch: {
      scripts: {
        files: [
          `${productRoot}/static/integration.js`,
          `${productRoot}/static/bundle.js`
        ],
        tasks: ['requirejs', 'uglify'],
        options: {
          livereload: true
        }
      },
      css: {
        files: `${productRoot}/static/integration.css`,
        tasks: ['cssmin'],
        options: {
          livereload: true
        }
      }
    }
  });

  grunt.registerTask('default', ['watch']);
  grunt.registerTask('compile', ['cssmin', 'requirejs', 'babel', 'uglify']);
};
