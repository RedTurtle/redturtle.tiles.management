# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from redturtle.tiles.management.testing import REDTURTLE_TILES_MANAGEMENT_INTEGRATION_TESTING  # noqa
from redturtle.tiles.management.tests.helpers import TestTile
from zope.event import notify
from zope.lifecycleevent import ObjectAddedEvent

import unittest2 as unittest


class TestTilesShowHide(unittest.TestCase):
    """Test that redturtle.tiles.management is properly installed."""

    layer = REDTURTLE_TILES_MANAGEMENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        api.user.create(
            username='editor',
            email='foo@bar.org',
            password='secret',
        )
        api.user.create(
            username='member',
            email='foo@bar.org',
            password='secret',
        )
        setRoles(self.portal, 'editor', ['Editor', 'Contributor'])
        setRoles(self.portal, 'member', ['Member'])

        self.document = api.content.create(
            type='Document',
            title='Test document',
            container=self.portal)
        # create two tiles
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
        notify(ObjectAddedEvent(tile, self.document, 'firstTile'))
        notify(ObjectAddedEvent(tile2, self.document, 'secondTile'))

    def test_anonymous_can_view_both(self):
        logout()
        tiles_view = api.content.get_view(
            name='tiles_management',
            context=self.document,
            request=self.request)
        self.assertEqual(len(tiles_view.get_tiles_list()), 2)

    def test_hide_tile(self):
        self.request.form = {
            'tileId': 'firstTile',
            'managerId': 'defaultManager',
        }

        tiles_view = api.content.get_view(
            name='tiles_management',
            context=self.document,
            request=self.request)
        show_hide_view = api.content.get_view(
            name='show_hide_tiles',
            context=self.document,
            request=self.request)
        # first hide a tile
        show_hide_view()

        self.assertEqual(len(tiles_view.get_tiles_list()), 2)
        logout()
        self.assertEqual(len(tiles_view.get_tiles_list()), 1)
