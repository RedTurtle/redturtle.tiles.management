# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import redturtle.tiles.management


class RedturtleTilesManagementLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=redturtle.tiles.management)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'redturtle.tiles.management:default')


REDTURTLE_TILES_MANAGEMENT_FIXTURE = RedturtleTilesManagementLayer()


REDTURTLE_TILES_MANAGEMENT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(REDTURTLE_TILES_MANAGEMENT_FIXTURE,),
    name='RedturtleTilesManagementLayer:IntegrationTesting',
)


REDTURTLE_TILES_MANAGEMENT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(REDTURTLE_TILES_MANAGEMENT_FIXTURE,),
    name='RedturtleTilesManagementLayer:FunctionalTesting',
)


REDTURTLE_TILES_MANAGEMENT_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        REDTURTLE_TILES_MANAGEMENT_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='RedturtleTilesManagementLayer:AcceptanceTesting',
)
