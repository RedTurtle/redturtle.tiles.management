# -*- coding: utf-8 -*-
from redturtle.tiles.management import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IRedturtleTilesManagementLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IRedturtleTilesManagementView(Interface):
    """Marker interface that defines a tiles management view."""


class ICreatedTile(Interface):
    """Marker interface for tiles. This is used to"""


class IRedturtleTilesManagementSettings(Interface):
    """ """
    enabled_tiles = schema.List(
        title=_(u'enabled_tiles_label',
                default=u'Enabled tiles'),
        description=_(u'enabled_tiles_help',
                      default=u'Select a list of tiles to add.'),
        required=False,
        default=[],
        missing_value=[],
        value_type=schema.Choice(
            vocabulary='tiles.management.vocabularies.RegisteredTiles',
        ),
    )

    tile_size_css_class = schema.List(
        title=_(u'size_css_classes',
                default=u'CSS Classes for tile sizes'),
        description=_(u'size_css_classes_descriptions',
                      default=u'List of CSS classes to resize the tile. '
                              u'These are used in the size button in tile '
                              u'management.\n'
                              u'The default style is "reset". It will add an '
                              u'empty string as CSS class and the tile will '
                              u'take the whole width.\n'
                              u'Insert a list of values (one per row) in the '
                              u'following form: display_name|css_class where '
                              u'display_name is the string to show to the user'
                              u' and css_class is the class will be applied '
                              u'to the tile'),
        required=False,
        default=[
            'reset|',
            'two tiles in a row|half-width',
        ],
        missing_value=[],
        value_type=schema.TextLine(),
    )
