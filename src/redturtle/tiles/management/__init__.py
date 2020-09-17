# -*- coding: utf-8 -*-
"""Init and utils."""
from Acquisition import aq_inner
from zope.i18nmessageid import MessageFactory
from plone.app.widgets import utils as widget_utils
from plone.app.tiles.browser.edit import AcquirableDictionary

import logging


_ = MessageFactory("redturtle.tiles.management")
logger = logging.getLogger("redturtle.tiles.management")


# patch to fix relateditems widgets (tiny and relation fields) start folder
def custom_get_relateditems_options(
    context,
    value,
    separator,
    vocabulary_name,
    vocabulary_view,
    field_name=None,
    include_recently_added=True,
):

    if isinstance(context, AcquirableDictionary):
        context = context.aq_parent
    else:
        # cleanup tiles acquisition on context
        context = aq_inner(context)
    return widget_utils._old_get_relateditems_options(
        context,
        value,
        separator,
        vocabulary_name,
        vocabulary_view,
        field_name,
        include_recently_added,
    )


logger.info("[PATCH] Applied get_relateditems_options patch")
widget_utils._old_get_relateditems_options = (
    widget_utils.get_relateditems_options
)
widget_utils.get_relateditems_options = custom_get_relateditems_options
