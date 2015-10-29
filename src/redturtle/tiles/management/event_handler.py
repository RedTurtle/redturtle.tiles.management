
from zope.annotation.interfaces import IAnnotations


def tileCreated(tile, event):
    context = event.newParent
    tile_id = event.newName
    if not context:
        return
    annotations = IAnnotations(context)
    if "tiles_list" not in annotations:
        annotations['tiles_list'] = []
    new_tile = {
        'tile_id': tile_id,
        'edit_url': tile.edit_url,
        'view_url': tile.url,
        'delete_url': tile.delete_url,
        }
    annotations['tiles_list'].append(new_tile)
