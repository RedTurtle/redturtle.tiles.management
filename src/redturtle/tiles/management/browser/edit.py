# -*- coding: utf-8 -*-
from plone.app.tiles.browser.edit import DefaultEditView
from plone.app.tiles.browser.edit import DefaultEditForm


class EditForm(DefaultEditForm):
    @property
    def action(self):
        """See interfaces.IInputForm"""
        if self.tileType and self.tileId and self.name:
            # PATCH #
            url = "{url}/@@edit-tile/{type}/{id}".format(
                url=self.context.absolute_url(),
                type=self.tileType.__name__,
                id=self.tileId,
            )
            # END OF PATCH #
        else:
            url = self.request.getURL()
        return url

    def nextURL(self, tile):
        return "{url}/{type}/{id}".format(
            url=self.context.absolute_url(), type=tile.__name__, id=tile.id,
        )


class EditView(DefaultEditView):
    form = EditForm
