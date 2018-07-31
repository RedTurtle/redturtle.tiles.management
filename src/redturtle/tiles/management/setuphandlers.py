# -*- coding: utf-8 -*-
from persistent.list import PersistentList
from persistent.mapping import PersistentMapping
from plone import api
from zope.annotation.interfaces import IAnnotations

import logging


logger = logging.getLogger(__name__)
default_profile = 'profile-redturtle.tiles.management:default'
uninstall_profile = 'profile-redturtle.tiles.management:uninstall'


def post_install(context):
    """Post install script"""
    if context.readDataFile('redturtletilesmanagement_default.txt') is None:
        return
    # Do something during the installation of this package


def uninstall(context):
    """Uninstall script"""
    if context.readDataFile('redturtletilesmanagement_uninstall.txt') is None:
        return
    # Do something during the uninstallation of this package


def update_tiles_list(brain):
    item = brain.getObject()
    annotations = IAnnotations(item)
    old_list = annotations.get('tiles_list', [])
    if not old_list:
        return
    new_list = PersistentList()
    for tile_infos in annotations.get('tiles_list', []):
        new_tile = PersistentMapping()
        new_tile['tile_id'] = tile_infos['tile_id']
        new_tile['tile_type'] = tile_infos['tile_type']
        new_tile['tile_hidden'] = False
        new_tile['tile_style'] = ''
        new_list.append(new_tile)

    # create new attribute and clear annotations
    item.tiles_list = PersistentMapping()
    item.tiles_list['defaultManager'] = new_list
    del annotations['tiles_list']
    logger.info('updated tiles list for: {0}'.format(brain.getPath()))


def to_1100(context):
    """
    """
    logger.info('Upgrading redturtle.tiles.management to version 1.0.0')
    context.runImportStepFromProfile(
        'profile-redturtle.tiles.management:to_1100', 'plone.app.registry')
    context.runImportStepFromProfile(default_profile, 'plone.app.registry')
    context.runImportStepFromProfile(default_profile, 'controlpanel')
    context.runImportStepFromProfile(default_profile, 'rolemap')
    context.runImportStepFromProfile(
        default_profile,
        'typeinfo',
        run_dependencies=True)
    logger.info('Reinstalled registry and controlpanel')
    portal = api.portal.get()
    for brain in portal.portal_catalog():
        update_tiles_list(brain)

    logger.info('migrated tiles')


def update_registry(context):
    """
    upgrade-step that updates registry
    """
    context.runImportStepFromProfile(default_profile, 'plone.app.registry')
