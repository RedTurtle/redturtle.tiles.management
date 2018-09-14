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
    postcss: {
      options: {
        map: {
          inline: false,
        },
        processors: [
          require('autoprefixer')({
            grid: true,
            browsers: ['last 2 versions', 'ie >= 11', 'iOS >= 6'],
          }),
          require('postcss-flexbugs-fixes')(),
        ]
      },
      dist: {
        src: [`${productRoot}/integration.css`],
      },
    },
    watch: {
      scripts: {
        files: [
          `${productRoot}/integration.js`,
          `${productRoot}/bundle.js`
        ],
        tasks: ['requirejs', 'babel', 'uglify'],
        options: {
          livereload: true
        }
      },
      css: {
        files: `${productRoot}/integration.css`,
        tasks: ['postcss', 'cssmin'],
        options: {
          livereload: true
        }
      }
    }
  });

  grunt.registerTask('default', ['watch']);
  grunt.registerTask('compile', ['postcss', 'cssmin', 'requirejs', 'babel', 'uglify']);
};
