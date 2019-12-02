# -*- coding: utf-8 -*-
from persistent.list import PersistentList
from persistent.mapping import PersistentMapping
from plone import api
from zope.annotation.interfaces import IAnnotations

import logging

logger = logging.getLogger(__name__)

default_profile = 'profile-redturtle.tiles.management:default'


def to_1100(context):
    """
    delete old registry configuration and add a new one
    """
    pc = api.portal.get_tool(name='portal_catalog')
    counter = 0
    for brain in pc():
        item = brain.getObject()
        try:
            annotations = IAnnotations(item)
        except TypeError:
            continue
        tiles_list = annotations.get('tiles_list', None)
        if not tiles_list:
            continue
        new_list = PersistentList()
        for tile in tiles_list:
            new_list.append(PersistentMapping(tile))
        annotations['tiles_list'] = new_list
        counter += 1
        logger.info('- {} Updated'.format(brain.getPath()))
    logger.info('Fixes {} items.'.format(counter))
