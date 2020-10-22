# -*- coding: utf-8 -*-
from plone.app.content.browser.vocabulary import SourceView as BaseView
from plone.app.tiles.browser.add import DefaultAddForm
from plone.app.tiles.browser.edit import DefaultEditForm
from plone import api


class SourceView(BaseView):
    def get_context(self):
        if isinstance(self.context.form, DefaultAddForm) or isinstance(
            self.context.form, DefaultEditForm
        ):
            # we are in a tile and the view is called in widget context and
            #  not in the portal root, so we need to set the context as root.
            return api.portal.get()
        return super(SourceView, self).get_context()
