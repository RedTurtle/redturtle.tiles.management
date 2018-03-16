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
from zope.security.interfaces import IPermission


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
        permissions_mapping = self.get_permissions()
        items = []
        enabled_tiles = api.portal.get_registry_record(
            'enabled_tiles', IRedturtleTilesManagementSettings)
        for item in vocabulary:
            if enabled_tiles and item.token not in enabled_tiles:
                # there is a list of selected tiles, and this one isn't
                # in the list
                continue
            can_add = api.user.has_permission(
                permissions_mapping.get(item.value.add_permission, ''),
                obj=context)
            if can_add:
                items.append(item)
        return SimpleVocabulary(items)

    def get_permissions(self):
        """
        generate a dict with all registered permissions, mapping like this:
        - key: permission id
        - value: permission name
        We need this because tiles add_permission is an id, but to check
        user permission we need the name.
        """
        return {
            x[0]: getattr(x[1], 'title', x[0])
            for x in getUtilitiesFor(IPermission, self.context)}
