from plone.app.tiles.browser.add import DefaultAddForm
from plone.app.tiles.browser.add import DefaultAddView


class AddForm(DefaultAddForm):
    def nextURL(self, tile):
        return "{url}/{type}/{id}".format(
            url=self.context.absolute_url(),
            type=tile.__name__,
            id=tile.id,
        )


class AddView(DefaultAddView):
    form = AddForm
