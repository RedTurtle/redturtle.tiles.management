# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.tiles.interfaces import ITile
from redturtle.tiles.management.testing import REDTURTLE_TILES_MANAGEMENT_INTEGRATION_TESTING  # noqa
from zope.event import notify
from zope.interface import implementer
from zope.lifecycleevent import ObjectAddedEvent
from zope.lifecycleevent import ObjectRemovedEvent
import unittest2 as unittest
# from zope.globalrequest import setRequest


@implementer(ITile)
class TestTile(object):

    def __init__(self, context, request, url, id):
        self.context = context
        self.request = request
        self.url = url
        self.id = id


class TestTilesCreation(unittest.TestCase):
    """Test that redturtle.tiles.management is properly installed."""

    layer = REDTURTLE_TILES_MANAGEMENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.document = api.content.create(
            type='Document',
            title='Test document',
            container=self.portal)

    def test_tile_creation(self):
        tile = TestTile(
            url='http://nohost/plone/test-document/@@my.tile/firstTile',
            id='firstTile',
            context=self.document,
            request=self.request)
        self.assertEqual(getattr(self.document, 'tiles_list', None), None)
        notify(ObjectAddedEvent(tile, self.document, tile.id))
        resStructure = {
            'default': [{'tile_type': 'my.tile', 'tile_id': 'firstTile'}]
        }
        self.assertEqual(self.document.tiles_list, resStructure)

        tile2 = TestTile(
            url='http://nohost/plone/test-document/@@alt.tile/secondTile',
            id='secondTile',
            context=self.document,
            request=self.request)
        notify(ObjectAddedEvent(tile2, self.document, tile2.id))
        resStructure['default'].append({
            'tile_type': 'alt.tile',
            'tile_id': 'secondTile'
        })
        self.assertEqual(self.document.tiles_list, resStructure)

    def test_tile_deletion(self):
        tile = TestTile(
            url='http://nohost/plone/test-document/@@my.tile/firstTile',
            id='firstTile',
            context=self.document,
            request=self.request)
        tile2 = TestTile(
            url='http://nohost/plone/test-document/@@alt.tile/secondTile',
            id='secondTile',
            context=self.document,
            request=self.request)
        # create two tiles
        notify(ObjectAddedEvent(tile, self.document, 'firstTile'))
        notify(ObjectAddedEvent(tile2, self.document, 'secondTile'))
        resStructure = {
            'default': [
                {'tile_type': 'my.tile', 'tile_id': 'firstTile'},
                {'tile_type': 'alt.tile', 'tile_id': 'secondTile'}
            ]
        }

        self.assertEqual(self.document.tiles_list, resStructure)
        # delete second tile
        notify(ObjectRemovedEvent(tile2, self.document, 'secondTile'))
        # remove it also from test structure
        resStructure['default'].pop()
        self.assertEqual(self.document.tiles_list, resStructure)
