# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.interface import Interface


class IRedturtleTilesManagementLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ICreatedTile(Interface):
    """Marker interface for tiles. This is used to"""
