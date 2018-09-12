# -*- coding: utf-8 -*-
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from redturtle.tiles.management.testing import REDTURTLE_TILES_MANAGEMENT_INTEGRATION_TESTING  # noqa

import unittest2 as unittest


class TestTilesManagement(unittest.TestCase):
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
        self.news = api.content.create(
            type='News Item',
            title='Test news',
            container=self.portal)

    def test_view_available_for_documents(self):
        doc_view = api.content.get_view(
            name='tiles_management',
            context=self.document,
            request=self.request)
        self.assertEqual(doc_view.__name__, 'tiles_management')

    def test_view_not_available_for_news(self):
        with self.assertRaises(InvalidParameterError):
            api.content.get_view(
                name='tiles_management',
                context=self.news,
                request=self.request)

    def test_anonymous_cant_add_new_tiles(self):
        logout()
        tiles_view = api.content.get_view(
            name='tiles_management',
            context=self.document,
            request=self.request)
        self.assertFalse(tiles_view.canManageTiles())
        login(self.portal, 'editor')

    def test_editor_can_add_new_tiles(self):
        login(self.portal, 'editor')
        tiles_view = api.content.get_view(
            name='tiles_management',
            context=self.document,
            request=self.request)
        self.assertTrue(tiles_view.canManageTiles())

    def test_anonymous_cant_edit_tiles(self):
        logout()
        tiles_view = api.content.get_view(
            name='tiles_management',
            context=self.document,
            request=self.request)
        self.assertFalse(tiles_view.canManageTiles())

    def test_editor_can_edit_tiles(self):
        login(self.portal, 'editor')
        tiles_view = api.content.get_view(
            name='tiles_management',
            context=self.document,
            request=self.request)
        self.assertTrue(tiles_view.canManageTiles())

    def test_extract_tiles_list(self):
        tiles_list = {
            'defaultManager': [
                {
                    'tile_id': 'firstTile',
                    'tile_type': 'my.tile',
                },
            ],
        }
        self.document.tiles_list = tiles_list
        tiles_view = api.content.get_view(
            name='tiles_management',
            context=self.document,
            request=self.request)
        self.assertEqual(
            tiles_view.get_tiles_list(),
            tiles_list['defaultManager'])

    def test_extract_tiles_list_selected_manager(self):
        tiles_list = {
            'defaultManager': [
                {
                    'tile_id': 'firstTile',
                    'tile_type': 'my.tile',
                },
            ],
            'alternative': [
                {
                    'tile_id': 'alternativeTile',
                    'tile_type': 'my.tile.alternative',
                },
                {
                    'tile_id': 'secondAlternativeTile',
                    'tile_type': 'my.othertile.alternative',
                },
            ],
        }
        self.document.tiles_list = tiles_list
        self.request.form['managerId'] = 'alternative'
        tiles_view = api.content.get_view(
            name='tiles_management',
            context=self.document,
            request=self.request)
        self.assertEqual(
            tiles_view.get_tiles_list(), tiles_list['alternative'])

    def test_extract_tile_url_from_infos(self):
        tile = {
            'tile_id': 'firstTile',
            'tile_type': 'my.tile',
        }
        tiles_view = api.content.get_view(
            name='tiles_management',
            context=self.document,
            request=self.request)
        self.assertEqual(
            tiles_view.get_tile_url(tile),
            './@@my.tile/firstTile')
