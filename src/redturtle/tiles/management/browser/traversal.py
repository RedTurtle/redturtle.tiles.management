# -*- coding: utf-8 -*-
try:
    # plone.app.tiles >= 3.*
    from plone.app.tiles import _
except ImportError:
    # plone.app.tiles < 3.*
    from plone.app.tiles import MessageFactory as _

from plone.app.tiles.browser.traversal import AddTile as BaseAddView
from plone.memoize.view import memoize
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory


class AddTile(BaseAddView):
    def keyfunction(self, tile):
        """Key for comparison by title"""
        return tile.title

    @memoize
    def tileTypes(self):
        """Get a list of addable ITileType objects representing tiles
        which are addable in the current context and selected in
        the registry configuration
        """
        tiles = []

        factory = getUtility(
            IVocabularyFactory,
            name="tiles.management.vocabularies.FilteredTiles",
        )
        vocabulary = factory(self.context)
        for item in vocabulary:
            tiletype = item.value
            # tile actions
            # TODO: read from registry  # noqa
            tiletype.actions = [
                {"name": "edit", "url": "@@edit-tile", "title": _("Edit")},
                {
                    "name": "remove",
                    "url": "@@delete-tile",
                    "title": _("Remove"),
                },
            ]
            tiles.append(tiletype)
        return sorted(tiles, key=self.keyfunction)
