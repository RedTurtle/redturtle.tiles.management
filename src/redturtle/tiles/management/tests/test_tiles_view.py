# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from redturtle.tiles.management.testing import REDTURTLE_TILES_MANAGEMENT_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import login, logout
import unittest2 as unittest
from plone.api.exc import InvalidParameterError


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
            name="tiles_management",
            context=self.document,
            request=self.request)
        self.assertEquals(doc_view.__name__, 'tiles_management')

    def test_view_not_available_for_news(self):
        with self.assertRaises(InvalidParameterError):
            api.content.get_view(
                name="tiles_management",
                context=self.news,
                request=self.request)

    def test_anonymous_cant_add_new_tiles(self):
        logout()
        tiles_view = api.content.get_view(
            name="tiles_management",
            context=self.document,
            request=self.request)
        self.assertFalse(tiles_view.canAddTiles())
        login(self.portal, 'editor')

    def test_editor_can_add_new_tiles(self):
        login(self.portal, 'editor')
        tiles_view = api.content.get_view(
            name="tiles_management",
            context=self.document,
            request=self.request)
        self.assertTrue(tiles_view.canAddTiles())

    def test_anonymous_cant_edit_tiles(self):
        logout()
        tiles_view = api.content.get_view(
            name="tiles_management",
            context=self.document,
            request=self.request)
        self.assertFalse(tiles_view.canEditTiles())

    def test_editor_can_edit_tiles(self):
        login(self.portal, 'editor')
        tiles_view = api.content.get_view(
            name="tiles_management",
            context=self.document,
            request=self.request)
        self.assertTrue(tiles_view.canEditTiles())
