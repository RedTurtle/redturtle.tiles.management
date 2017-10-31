# -*- coding: utf-8 -*-
from plone import api
from plone.app.blocks.interfaces import IBlocksTransformEnabled
from plone.memoize import view
from plone.protect.authenticator import createToken
from Products.Five import BrowserView
from zope.annotation.interfaces import IAnnotations
from zope.interface import implementer

import json


@implementer(IBlocksTransformEnabled)
class BaseView(BrowserView):
    '''
    '''

    @view.memoize
    def get_tiles_list(self):
        annotations = IAnnotations(self.context)
        return annotations.get('tiles_list', [])

    def get_json_tiles(self):
        if api.user.is_anonymous():
            return ""
        current = api.user.get_current()
        if api.user.has_permission(
            'Modify portal content',
            user=current,
            obj=self.context):
            return json.dumps(self.get_tiles_list())
        return ""

    def canManageTiles(self):
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

    def getToken(self):
        return createToken()


class ReorderTilesView(BrowserView):
    '''
    '''

    def __call__(self):
        if not self.request.form.get('tile_ids'):
            return ""
        try:
            sorted_ids = json.loads(self.request.form.get('tile_ids'))
            annotations = IAnnotations(self.context)
            order_dict = {tile_id: index for index, tile_id in enumerate(sorted_ids)}
            annotations['tiles_list'].sort(
                key=lambda x: order_dict[x["tile_id"]])
            return ""
        except ValueError as e:
            return json.dumps({'error': e.message})
