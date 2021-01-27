# -*- coding: utf-8 -*-
from plone.app.tiles.browser.delete import DefaultDeleteView
from plone.app.tiles.browser.delete import DefaultDeleteForm
from plone.app.tiles import _
from plone.tiles.interfaces import ITileDataManager
from Products.statusmessages.interfaces import IStatusMessage
from zope.event import notify
from zope.lifecycleevent import ObjectRemovedEvent
from zope.traversing.browser import absoluteURL
from z3c.form import button

import logging

logger = logging.getLogger(__name__)


class DeleteForm(DefaultDeleteForm):
    @property
    def action(self):
        """See interfaces.IInputForm"""
        if self.tileType and self.tileId and self.name:
            # PATCH #
            url = "{url}/@@delete-tile/{type}/{id}".format(
                url=self.context.absolute_url(),
                type=self.tileType.__name__,
                id=self.tileId,
            )
            # END OF PATCH #
        else:
            url = self.request.getURL()
        return url

    @button.buttonAndHandler(_("Delete"), name="delete")
    def handleDelete(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        typeName = self.tileType.__name__

        # Traverse to the tile about to be removed
        tile = self.context.restrictedTraverse(
            "@@%s/%s" % (typeName, self.tileId,)
        )
        # Look up the URL - we need to do this before we've deleted the data to
        # correctly account for transient tiles
        tileURL = absoluteURL(tile, self.request)

        dataManager = ITileDataManager(tile)
        dataManager.delete()

        # PATCH #
        key = "{}/{}".format(typeName, self.tileId)
        if key in dataManager.storage.keys():
            # this is a not persistent tile and we need to force deletion
            dataManager.storage[key] = {}
        # END OF PATCH #

        notify(ObjectRemovedEvent(tile, self.context, self.tileId))
        logger.debug(u"Tile deleted at {0}".format(tileURL))

        # Skip form rendering for AJAX requests
        if self.request.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
            IStatusMessage(self.request).addStatusMessage(
                _(u"Tile deleted at ${url}", mapping={"url": tileURL}),
                type=u"info",
            )
            self.template = lambda: u""
            return

        try:
            url = self.nextURL(tile)
        except NotImplementedError:
            url = self.context.absolute_url()

        self.request.response.redirect(url)

    @button.buttonAndHandler(_(u"Cancel"), name="cancel")
    def handleCancel(self, action):
        super(DeleteForm, self).handleCancel(action)


class DeleteView(DefaultDeleteView):
    form = DeleteForm
