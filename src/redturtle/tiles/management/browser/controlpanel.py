# -*- coding: utf-8 -*-
from plone.app.registry.browser import controlpanel
from redturtle.tiles.management.interfaces import IRedturtleTilesManagementSettings
from redturtle.tiles.management import _


class RedturtleTilesManagementEditForm(controlpanel.RegistryEditForm):
    """settings form."""
    schema = IRedturtleTilesManagementSettings
    id = "TilesManagementSettingsEditForm"
    label = _('tiles_management_settings_label', u'Tiles Management Settings')
    description = u""


class RedturtleTilesManagementSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    """Analytics settings control panel.
    """
    form = RedturtleTilesManagementEditForm
