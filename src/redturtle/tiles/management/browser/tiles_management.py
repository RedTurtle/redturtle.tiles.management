# -*- coding: utf-8 -*-
from Acquisition import aq_base
from plone import api
from plone.app.blocks.interfaces import IBlocksTransformEnabled
from plone.memoize import view
from Products.Five import BrowserView
from zope.interface import implementer, implements
import json
from redturtle.tiles.management.interfaces import IRedturtleTilesManagementView

import logging
logger = logging.getLogger(__name__)


@implementer(IBlocksTransformEnabled)
class BaseView(BrowserView):
    '''
    '''

    implements(IRedturtleTilesManagementView)

    @view.memoize
    def get_tiles_list(self):
        tiles_list = getattr(self.context, 'tiles_list', {})
        managerId = self.request.form.get('managerId', 'default')
        # it's a PersistentList
        return list(tiles_list.get(managerId, []))

    def extractTileInfos(self, key):
        type, id = key.split('/')
        return {
            'tile_id': id,
            'tile_type': type
        }

    def canEditTiles(self):
        if api.user.is_anonymous():
            return False
        current = api.user.get_current()
        return api.user.has_permission(
            'Modify portal content',
            user=current,
            obj=self.context)

    def canAddTiles(self):
        if api.user.is_anonymous():
            return False
        current = api.user.get_current()
        return api.user.has_permission(
            'Modify portal content',
            user=current,
            obj=self.context)

    def get_tile_url(self, tile):
        return "%s/@@%s/%s" % (
            self.context.absolute_url(),
            tile.get('tile_type'),
            tile.get('tile_id'))


class ReorderTilesView(BrowserView):
    '''
    '''

    def __call__(self):
        tileIds = self.request.form.get('tileIds')
        managerId = self.request.form.get('managerId', 'default')
        if not tileIds:
            return ""

        context = aq_base(self.context)
        tiles_list = getattr(context, 'tiles_list', None)
        if not tiles_list:
            return ""
        tilesForManager = tiles_list.get(managerId)
        if not tilesForManager:
            return ""
        try:
            sorted_ids = json.loads(tileIds)
            order_dict = {
                tile_id: index for index, tile_id in enumerate(sorted_ids)
            }
            tilesForManager.sort(key=lambda x: order_dict[x["tile_id"]])
            # tilesForManager = tiles_list
            return ""
        except ValueError as e:
            logger.trace(e)
            return json.dumps({'error': e.message})
