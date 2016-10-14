# -*- coding: utf-8 -*-
from plone import api
from plone.app.tiles.browser.add import DefaultAddForm
from plone.app.tiles.browser.add import DefaultAddView
from plone.app.tiles.browser.delete import DefaultDeleteForm
from plone.app.tiles.browser.delete import DefaultDeleteView
from plone.app.tiles.browser.edit import DefaultEditForm
from plone.app.tiles.browser.edit import DefaultEditView
from plone.uuid.interfaces import IUUIDGenerator
from zope.component import getUtility
from zope.event import notify
from zope.lifecycleevent import ObjectAddedEvent
from zope.lifecycleevent import ObjectCreatedEvent
from plone.tiles.interfaces import ITileDataManager
from redturtle.tiles.management import _
from redturtle.tiles.management import logger
from z3c.form import button
from zope.lifecycleevent import ObjectModifiedEvent
from zope.traversing.browser.absoluteurl import absoluteURL


class TilesAddForm(DefaultAddForm):

    def nextURL(self, tile=None):
        return self.context.absolute_url()

    # Buttons/actions

    @button.buttonAndHandler(_('Save'), name='save')
    def handleAdd(self, action):

        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        typeName = self.tileType.__name__

        generator = getUtility(IUUIDGenerator)
        tileId = generator()

        # Traverse to a new tile in the context, with no data
        tile = self.context.restrictedTraverse(
            '@@%s/%s' % (typeName, tileId,))

        dataManager = ITileDataManager(tile)
        dataManager.set(data)

        # Look up the URL - we need to do this after we've set the data to
        # correctly account for transient tiles
        tileURL = absoluteURL(tile, self.request)

        notify(ObjectCreatedEvent(tile))
        notify(ObjectAddedEvent(tile, self.context, tileId))
        logger.debug(u"Tile created at {0}".format(tileURL))

        try:
            url = self.nextURL(tile)
        except NotImplementedError:
            url = tileURL

        api.portal.show_message(
            message=_('Tile added'),
            request=self.request)
        self.request.response.redirect(url)

    @button.buttonAndHandler(_(u'Cancel'), name='cancel')
    def handleCancel(self, action):
        api.portal.show_message(
            message=_('Tile add cancelled'),
            request=self.request)
        self.request.response.redirect(self.nextURL())


class TilesAddView(DefaultAddView):
    """
    Overrides default add view
    """
    form = TilesAddForm


class TilesEditForm(DefaultEditForm):

    def nextURL(self, tile=None):
        return self.context.absolute_url()

    # Buttons/actions

    @button.buttonAndHandler(_('Save'), name='save')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        typeName = self.tileType.__name__

        # Traverse to a new tile in the context, with no data
        tile = self.context.restrictedTraverse(
            '@@%s/%s' % (typeName, self.tileId,))

        dataManager = ITileDataManager(tile)
        dataManager.set(data)

        # Look up the URL - we need to do this after we've set the data to
        # correctly account for transient tiles
        tileURL = absoluteURL(tile, self.request)

        notify(ObjectModifiedEvent(tile))
        logger.debug(u"Tile edited at {0}".format(tileURL))

        try:
            url = self.nextURL(tile)
        except NotImplementedError:
            url = tileURL
        api.portal.show_message(
            message=_('Tile edited'),
            request=self.request)
        self.request.response.redirect(url)

    @button.buttonAndHandler(_(u'Cancel'), name='cancel')
    def handleCancel(self, action):
        api.portal.show_message(
            message=_('Tile edit cancelled'),
            request=self.request)
        self.request.response.redirect(self.nextURL())


class TilesEditView(DefaultEditView):
    """
    Overrides default add view
    """
    form = TilesEditForm


class TilesDeleteForm(DefaultDeleteForm):

    def nextURL(self, tile=None):
        return self.context.absolute_url()

    @button.buttonAndHandler(_('Delete'), name='delete')
    def handleDelete(self, action):
        super(TilesDeleteForm, self).handleDelete(self, action)

    def updateActions(self):
        super(DefaultDeleteForm, self).updateActions()
        self.actions["delete"].addClass("context")


class TilesDeleteView(DefaultDeleteView):
    """
    Overrides default delete view
    """
    form = TilesDeleteForm
