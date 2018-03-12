# -*- coding: utf-8 -*-
from plone.app.registry.browser import controlpanel
from redturtle.tiles.management import _
from redturtle.tiles.management.interfaces import IRedturtleTilesManagementSettings  # noqa


class RedturtleTilesManagementEditForm(controlpanel.RegistryEditForm):
    """settings form."""
    schema = IRedturtleTilesManagementSettings
    id = 'TilesManagementSettingsEditForm'
    label = _('tiles_management_settings_label', u'Tiles Management Settings')
    description = u''


class RedturtleTilesManagementSettingsControlPanel(controlpanel.ControlPanelFormWrapper):  # noqa
    """Analytics settings control panel.
    """
    form = RedturtleTilesManagementEditForm
