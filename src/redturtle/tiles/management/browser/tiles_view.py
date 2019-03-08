# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.blocks.interfaces import IBlocksTransformEnabled
from zope.interface import implementer


@implementer(IBlocksTransformEnabled)
class TilesView(BrowserView):
    index = ViewPageTemplateFile("templates/tiles_view.pt")

    def __call__(self, **kwargs):
        return self.index()
