.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide_addons.html
   This text does not appear on pypi or github. It is a comment.

==============================================================================
redturtle.tiles.management
==============================================================================

A tiles management system, easier than plone.app.mosaic that uses
`plone.app.tiles`__ and `Mockup`__ functionalities to build a simple UI.

__ https://github.com/plone/plone.app.tiles
__ https://github.com/plone/mockup

Features
--------

- Simple UI to add/remove/edit registered tiles
- Tiles sorting with drag-and-drop (thanks to mockup)
- Base view and macro to be reused in custom templates

Usage
-----

To use this feature, you only need to do 2 simple steps:

1) Make you view implements IBlocksTransformEnabled interface::

    from plone.app.blocks.interfaces import IBlocksTransformEnabled
    from Products.Five import BrowserView
    from zope.interface import implementer

    @implementer(IBlocksTransformEnabled)
    class MyView(BrowserView):
        ...

2) use a specific macro in the template, where you want to insert the tiles::

    <tal:tiles metal:use-macro="context/tiles_view/macros/tiles-macro" />

3) the used tiles need to expose their id to allows the UI to handle correct actions::

    <div data-tileid="${view/id}">
      .. your tile html
    </div>

The last point can be improved because with this restriction we can't use standard tiles, but only custom tiles.

After this, you see a new "Add tile" button in the view, and clicking on it,
you can see a list of available tiles.

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

For Plone 4 there is an additional javascript with some mockup's patterns used for
drag and drop behavior.

You need to include two javascripts in your view template or register them in
the global jsregistry. I don't want to register globally these resources
because they are used only in one single view:

- `++resource++rer.giovazoom.plonetheme.javascripts/mockup.js`
- `++resource++redturtle.tiles.management/integration.js`


Contribute
----------

- Issue Tracker: https://github.com/RedTurtle/redturtle.tiles.management/issues
- Source Code: https://github.com/RedTurtle/redturtle.tiles.management


License
-------

The project is licensed under the GPLv2.
