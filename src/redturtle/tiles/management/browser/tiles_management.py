# -*- coding: utf-8 -*-
from Acquisition import aq_base
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.blocks.interfaces import IBlocksTransformEnabled
from plone.protect.authenticator import createToken
from Products.Five import BrowserView
from redturtle.tiles.management.interfaces import IRedturtleTilesManagementView
from redturtle.tiles.management.interfaces import IRedturtleTilesManagementSettings # noqa
from zope.interface import implementer

import json
import logging


logger = logging.getLogger(__name__)


@implementer(IBlocksTransformEnabled, IRedturtleTilesManagementView)
class BaseView(BrowserView):
    """
    """

    def get_tiles_list(self):
        tiles_list = getattr(self.context, 'tiles_list', {})
        managerId = self.request.form.get('managerId', 'defaultManager')
        # it's a PersistentList
        tiles = tiles_list.get(managerId, [])
        can_manage = self.canManageTiles()
        return [x for x in tiles if (not x.get('tile_hidden') or can_manage)]

    def extractTileInfos(self, key):
        type, id = key.split('/')
        return {
            'tile_id': id,
            'tile_type': type,
        }

    def canManageTiles(self):
        if api.user.is_anonymous():
            return False
        current = api.user.get_current()
        return api.user.has_permission(
            'tiles management: Manage Tiles',
            user=current,
            obj=self.context)

    def get_tile_url(self, tile):
        return './@@{0}/{1}'.format(
            tile.get('tile_type'),
            tile.get('tile_id'))

    def get_tile_size_settings(self):
        try:
            return api.portal.get_registry_record(
                'tile_size_css_class',
                interface=IRedturtleTilesManagementSettings,
            )
        except InvalidParameterError:
            logger.info('ciao')
            return []

    def get_tile_size_classes(self):
        sizes = self.get_tile_size_settings()
        res = []
        for size in sizes:
            try:
                display_name, css_class = size.split('|')
                res.append({
                    'display_name': display_name,
                    'css_class': css_class,
                })
            except ValueError:
                logger.warning(
                        '[RedTurtle Tiles Management Tile Size Classes] '
                        '- skipped entry "{0}"'
                        ' because is malformed. Check it in control panel.')
                continue
        return res

    def getToken(self):
        return createToken()


class ReorderTilesView(BrowserView):
    """
    """

    def __call__(self):
        tileIds = self.request.form.get('tileIds')
        managerId = self.request.form.get('managerId', 'defaultManager')
        if not tileIds:
            return ''

        context = aq_base(self.context)
        tiles_list = getattr(context, 'tiles_list', None)
        if not tiles_list:
            return ''
        tilesForManager = tiles_list.get(managerId)
        if not tilesForManager:
            return ''
        try:
            sorted_ids = json.loads(tileIds)
            order_dict = {
                tile_id: index for index, tile_id in enumerate(sorted_ids)
            }
            tilesForManager.sort(key=lambda x: order_dict[x['tile_id']])
            # tilesForManager = tiles_list
            return ''
        except ValueError as e:
            logger.trace(e)
            return json.dumps({'error': e.message})


class ShowHideTilesView(BrowserView):
    """
    """

    def __call__(self):
        tileId = self.request.form.get('tileId')
        managerId = self.request.form.get('managerId', 'defaultManager')
        if not tileId:
            return ''

        context = aq_base(self.context)
        tiles_list = getattr(context, 'tiles_list', None)
        if not tiles_list:
            return ''
        try:
            for tile in tiles_list.get(managerId, []):
                if tile.get('tile_id') == tileId:
                    # toggle hidden mode
                    tile['tile_hidden'] = not tile.get('tile_hidden', False)
            return ''
        except Exception as e:
            logger.exception(e)
            return json.dumps({'error': e.message})


class ResizeTilesView(BrowserView):
    """
    Adds data to the wrapper to handle sizes (i.e.: in columns), which can be
    defined in the control panel
    """

    def __call__(self):
        tileId = self.request.form.get('tileId')
        managerId = self.request.form.get('managerId', 'defaultManager')
        style = self.request.form.get('style', '')

        if not tileId:
            return ''

        context = aq_base(self.context)
        tiles_list = getattr(context, 'tiles_list', None)

        if not tiles_list:
            return ''

        try:
            for tile in tiles_list.get(managerId, []):
                if tile.get('tile_id') == tileId:
                    tile['tile_style'] = style
            return ''
        except Exception as e:
            logger.exception(e)
            return json.dumps({'error': e.message})
