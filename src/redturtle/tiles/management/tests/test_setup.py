# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.browserlayer import utils
from redturtle.tiles.management.interfaces import IRedturtleTilesManagementLayer  # noqa
from redturtle.tiles.management.testing import REDTURTLE_TILES_MANAGEMENT_INTEGRATION_TESTING  # noqa

import unittest2 as unittest


class TestSetup(unittest.TestCase):
    """Test that redturtle.tiles.management is properly installed."""

    layer = REDTURTLE_TILES_MANAGEMENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """
        Test if redturtle.tiles.management is installed
        with portal_quickinstaller.
        """
        self.assertTrue(
            self.installer.isProductInstalled('redturtle.tiles.management'))

    def test_browserlayer(self):
        """Test that IRedturtleTilesManagementLayer is registered."""
        self.assertIn(
            IRedturtleTilesManagementLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = REDTURTLE_TILES_MANAGEMENT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['redturtle.tiles.management'])

    def test_product_uninstalled(self):
        """Test if redturtle.tiles.management is cleanly uninstalled."""
        self.assertFalse(
            self.installer.isProductInstalled('redturtle.tiles.management'))

    def test_browserlayer_removed(self):
        """Test that IRedturtleTilesManagementLayer is removed."""
        self.assertNotIn(
            IRedturtleTilesManagementLayer, utils.registered_layers())
