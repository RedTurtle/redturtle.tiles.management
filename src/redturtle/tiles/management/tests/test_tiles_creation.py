# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from redturtle.tiles.management.testing import REDTURTLE_TILES_MANAGEMENT_INTEGRATION_TESTING  # noqa
from redturtle.tiles.management.tests.helpers import TestTile
from zope.event import notify
from zope.lifecycleevent import ObjectAddedEvent
from zope.lifecycleevent import ObjectRemovedEvent

import unittest2 as unittest


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
            'defaultManager': [
                {
                    'tile_type': 'my.tile',
                    'tile_id': 'firstTile',
                    'tile_hidden': False,
                    'tile_style': '',
                },
            ],
        }
        self.assertEqual(self.document.tiles_list, resStructure)

        tile2 = TestTile(
            url='http://nohost/plone/test-document/@@alt.tile/secondTile',
            id='secondTile',
            context=self.document,
            request=self.request)
        notify(ObjectAddedEvent(tile2, self.document, tile2.id))
        resStructure['defaultManager'].append({
            'tile_type': 'alt.tile',
            'tile_id': 'secondTile',
            'tile_hidden': False,
            'tile_style': '',
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
            'defaultManager': [
                {
                    'tile_type': 'my.tile',
                    'tile_id': 'firstTile',
                    'tile_hidden': False,
                    'tile_style': '',
                },
                {
                    'tile_type': 'alt.tile',
                    'tile_id': 'secondTile',
                    'tile_hidden': False,
                    'tile_style': '',
                },
            ],
        }

        self.assertEqual(self.document.tiles_list, resStructure)
        # delete second tile
        notify(ObjectRemovedEvent(tile2, self.document, 'secondTile'))
        # remove it also from test structure
        resStructure['defaultManager'].pop()
        self.assertEqual(self.document.tiles_list, resStructure)
