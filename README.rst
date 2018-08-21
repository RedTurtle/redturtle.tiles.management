.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide_addons.html
   This text does not appear on pypi or github. It is a comment.

==============================================================================
redturtle.tiles.management
==============================================================================

.. image:: https://travis-ci.org/RedTurtle/redturtle.tiles.management.svg?branch=master
    :target: https://travis-ci.org/RedTurtle/redturtle.tiles.management

A tiles management system, easier than plone.app.mosaic that uses
`plone.app.tiles`__ and `Mockup`__ functionalities to build a simple UI.

__ https://github.com/plone/plone.app.tiles
__ https://github.com/plone/mockup

Features
--------

- Simple UI to add/remove/edit registered tiles
- Tiles sorting with drag-and-drop (thanks to mockup)
- Tiles resizing (with default or custom CSS classes)
- Tile manager is a pattern that can be included in every custom page
- **plone.layoutaware** behavior enabled for Documents
- Example *tiles_view* view available for all objects with "plone.layoutaware" behavior enabled
- Customizable available tiles list from control panel

Usage
-----

Tiles manager works with plone.app.blocks features and its plone.layoutaware behavior, so you can use this functionality
only on Content Types with this behavior enabled.

Installing this product, a new pattern will be available: "*pat-tiles-management*", and you only need to insert a pattern-style tag into your view like this:

.. code-block:: html

  <div class="pat-tiles-management" data-pat-tiles-management="managerId:myManager" />

You need to provide a **managerId** attribute, because multiple managers can be instantiated in a view, and with this, the pattern can handle the tiles stored in each manager.


Available tiles list
--------------------

You can configure a list of addable tiles for this manager in Plone's control panel:
http://yoursite/@@tiles-management-settings

In the "Add new tile" menu you'll see this list filtered also by single tiles permission.


Tile resizing
-------------

If you want two tiles in a row, from tile control buttons select a style in the "resize" dropdown.
There are two default styles:

- reset (with no CSS classes)
- two tiles in a row (`half-width` class)

These CSS classes can be configured in control panel.


JS Development and bundling
---------------------------

If you need to develop this product's javascripts or styles, you need to compile the code
for the resource registry bundle. To do this, there are two grunt tasks.

First of all, you need to install grunt dependencies listed in package.json file in the root of this package:

.. code-block:: shell

  npm install

or if you prefer yarn:

.. code-block:: shell

  yarn

After that, you can use two different grunt tasks:

- `grunt`: the default task, that listen files changes with `watch` and re-build resources and bundles automatically
- `grunt compile`: to manually compile all resources and bundles


Translations
------------

This product has been translated into

- Italian


Installation
------------

Install redturtle.tiles.management by adding it to your buildout::

   [buildout]

    ...

    eggs =
        redturtle.tiles.management


and then running "bin/buildout"


Compatibility
-------------
This package is developed with mockup, so is fully compatible for Plone 5.

From 1.0.0 version, Plone 4 compatibility has been dropped, so you need to use the 0.x branch.

Contribute
----------

- Issue Tracker: https://github.com/RedTurtle/redturtle.tiles.management/issues
- Source Code: https://github.com/RedTurtle/redturtle.tiles.management


License
-------

The project is licensed under the GPLv2.
