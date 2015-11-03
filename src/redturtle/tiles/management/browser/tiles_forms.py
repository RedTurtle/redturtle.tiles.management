# -*- coding: utf-8 -*-
from plone.app.tiles.browser.add import DefaultAddView
from plone.app.tiles.browser.add import DefaultAddForm
from plone.app.tiles.browser.edit import DefaultEditView
from plone.app.tiles.browser.edit import DefaultEditForm
from plone.app.tiles.browser.delete import DefaultDeleteView
from plone.app.tiles.browser.delete import DefaultDeleteForm


class TilesAddForm(DefaultAddForm):

    def nextURL(self, tile):
        return self.context.absolute_url()


class TilesAddView(DefaultAddView):
    """
    Overrides default add view
    """
    form = TilesAddForm


class TilesEditForm(DefaultEditForm):

    def nextURL(self, tile):
        return self.context.absolute_url()


class TilesEditView(DefaultEditView):
    """
    Overrides default add view
    """
    form = TilesEditForm


class TilesDeleteForm(DefaultDeleteForm):

    def nextURL(self, tile):
        return self.context.absolute_url()


class TilesDeleteView(DefaultDeleteView):
    """
    Overrides default delete view
    """
    form = TilesDeleteForm
