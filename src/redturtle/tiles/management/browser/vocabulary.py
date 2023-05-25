# -*- coding: utf-8 -*-
from AccessControl import getSecurityManager
from plone import api
from plone.app.content.browser.vocabulary import SourceView as BaseView
from plone.app.content.browser.vocabulary import VocabLookupException
from plone.app.tiles.browser.add import DefaultAddForm
from plone.app.tiles.browser.edit import DefaultEditForm
from plone.autoform.interfaces import WRITE_PERMISSIONS_KEY
from plone.supermodel.utils import mergedTaggedValueDict
from zope.component import getUtility
from zope.component import queryUtility
from zope.schema.interfaces import ICollection
from zope.security.interfaces import IPermission


class SourceView(BaseView):
    def get_context(self):
        if isinstance(self.context.form, DefaultAddForm) or isinstance(
            self.context.form, DefaultEditForm
        ):
            # we are in a tile and the view is called in widget context and
            #  not in the portal root, so we need to set the context as root.
            return api.portal.get()
        return super(SourceView, self).get_context()

    def get_vocabulary(self):
        widget = self.context
        field = widget.field.bind(widget.context)

        # check field's write permission
        info = mergedTaggedValueDict(field.interface, WRITE_PERMISSIONS_KEY)
        permission_name = info.get(field.__name__, "cmf.ModifyPortalContent")
        permission = queryUtility(IPermission, name=permission_name)
        if permission is None:
            permission = getUtility(IPermission, name="cmf.ModifyPortalContent")
        if not getSecurityManager().checkPermission(
            permission.title,
            self.context.context,  # this is the patch
        ):
            raise VocabLookupException("Vocabulary lookup not allowed.")

        if ICollection.providedBy(field):
            return field.value_type.vocabulary
        return field.vocabulary
