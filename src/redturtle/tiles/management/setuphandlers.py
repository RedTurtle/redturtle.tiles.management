from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles:
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "redturtle.tiles.management:uninstall",
            "redturtle.tiles.management:to_1100",
            "redturtle.tiles.management:to_2000",
        ]


def post_install(context):
    """Post install script"""
    if context.readDataFile("redturtletilesmanagement_default.txt") is None:
        return
    # Do something during the installation of this package


def uninstall(context):
    """Uninstall script"""
    if context.readDataFile("redturtletilesmanagement_uninstall.txt") is None:
        return
    # Do something during the uninstallation of this package
