# -*- coding: utf-8 -*-
from plone import api
from plone.app.tiles.vocabularies import AvailableTilesVocabulary
from plone.tiles.interfaces import ITileType
from redturtle.tiles.management.interfaces import IRedturtleTilesManagementSettings  # noqa
from zope.component import getUtilitiesFor
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class RegisteredTilesIdsVocabulary(object):
    """
    Return vocabulary with all enabled tiles
    """

    def __call__(self, context=None):
        context = context or self.context
        items = []
        tiles = getUtilitiesFor(ITileType, context=context)

        for name, tile in tiles:
            items.append(SimpleTerm(name, name, tile.title))
        return SimpleVocabulary(items)


@implementer(IVocabularyFactory)
class FilteredTilesVocabulary(AvailableTilesVocabulary):
    """
    Return vocabulary of all tiles with allowed add permission
    and enabled in controlpanel
    """

    def __call__(self, context=None):
        context = self.context or context
        vocabulary = super(FilteredTilesVocabulary, self).__call__(context)
        # first get all allowed tiles
        if context is None:
            return vocabulary

        items = []
        enabled_tiles = api.portal.get_registry_record(
            'enabled_tiles', IRedturtleTilesManagementSettings)
        for item in vocabulary:
            if enabled_tiles and item.token not in enabled_tiles:
                # there is a list of selected tiles, and this one isn't
                # in the list
                continue
            if api.user.has_permission(item.value.add_permission, obj=context):
                items.append(item)
        return SimpleVocabulary(items)
