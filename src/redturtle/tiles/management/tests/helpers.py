# -*- coding: utf-8 -*-
from plone.tiles.interfaces import ITile
from zope.interface import implementer


@implementer(ITile)
class TestTile(object):

    def __init__(self, context, request, url, id):
        self.context = context
        self.request = request
        self.url = url
        self.id = id
