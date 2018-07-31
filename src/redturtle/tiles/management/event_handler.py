# -*- coding: utf-8 -*-
from Acquisition import aq_base
from persistent.list import PersistentList
from persistent.mapping import PersistentMapping

import re


def getManagerId(tile):
    managerId = tile.request.form.get('managerId')
    if not managerId:
        managerId = 'defaultManager'
    return managerId


def tileCreated(tile, event):
    # avoid attributes acquisition
    context = aq_base(event.newParent)
    tile_id = event.newName
    if not context:
        return

    managerId = getManagerId(tile)

    new_tile = PersistentMapping()
    new_tile['tile_id'] = tile_id
    new_tile['tile_hidden'] = False
    new_tile['tile_style'] = ''

    try:
        tile_type = re.search('@@(.*?)/', tile.url).group(1)
    except AttributeError:
        tile_type = ''
    if tile_type:
        new_tile['tile_type'] = tile_type

    # store tiles_order in persistent object attribute.
    if not getattr(context, 'tiles_list', {}):
        context.tiles_list = PersistentMapping()
    if managerId not in context.tiles_list:
        context.tiles_list[managerId] = PersistentList()
    context.tiles_list[managerId].append(new_tile)


def tileDeleted(tile, event):
    context = aq_base(tile.context)
    managerId = getManagerId(tile)
    tiles_list = getattr(context, 'tiles_list', {})
    if not tiles_list:
        return
    tilesForManager = tiles_list.get(managerId, [])
    if not tilesForManager:
        return
    for tile_info in tilesForManager:
        if tile_info.get('tile_id') == tile.id:
            context.tiles_list[managerId].remove(tile_info)
