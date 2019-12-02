# -*- coding: utf-8 -*-
from persistent.list import PersistentList
from persistent.mapping import PersistentMapping
from zope.annotation.interfaces import IAnnotations

import re


def tileCreated(tile, event):
    context = event.newParent
    tile_id = event.newName
    if not context:
        return
    annotations = IAnnotations(context)
    if "tiles_list" not in annotations:
        annotations['tiles_list'] = PersistentList()

    new_tile = PersistentMapping()
    new_tile['tile_id'] = tile_id

    try:
        tile_type = re.search("@@(.*?)/", tile.url).group(1)
    except AttributeError:
        tile_type = ""
    if tile_type:
        new_tile['tile_type'] = tile_type
    annotations['tiles_list'].append(new_tile)


def tileDeleted(tile, event):
    annotations = IAnnotations(tile.context)
    for tile_info in annotations.get('tiles_list', []):
        if tile_info.get('tile_id') == tile.id:
            annotations['tiles_list'].remove(tile_info)
