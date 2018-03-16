Changelog
=========


1.1.2 (2018-03-16)
------------------

- Fix permission checks in addable tiles vocabulary.
  Now use correct permission (name) and not the id.
  [cekk]


1.1.1 (2018-03-12)
------------------

- Fix pypi brown bag release
  [cekk]

1.1.0 (2018-03-12)
------------------

- Add a loader when tiles are fetched
  [cekk]
- Remove empty managers when user can't add tiles
  [cekk]
- Refactor manager render view. Now is lighter (no more unused Plone body macros)
  and can be used also in static renders
  [cekk]

1.0.2 (2017-12-21)
------------------

- Fix IE11 compatibility: add babel-polyfill to correctly handle CustomEvent raise
  [cekk]


1.0.1 (2017-09-13)
------------------

- Fix README code syntax
  [cekk]

1.0.0 (2017-09-13)
------------------

- Massive changes in tiles storing (with p.a.blocks plone.layoutaware behavior)
  and in tiles management: now it's a pattern that can be instantiated several
  times in the view
  [cekk]
- Add controlpanel to configure a list of addable tiles from registered ones.
  [cekk]
- Add icon and button color for action hide tile [nekorin]
- Handle error message when there are problems fetching tiles
  [cekk]
- Added an event dispatched when tiles are added to the DOM [nzambello]
- Drop support for Plone4. Use branch 0.x for Plone 4
  [cekk]

0.2.1 (2017-04-12)
------------------

- Fixed resources import in tiles_view [pnicolli]
- Fixed rolemap. Permission to edit tiles given to 'Editor' #10460 [arsenico13]
- .DS_Store added to .gitignore and MANIFEST [arsenico13]
- Fixed tiles edit link. This fixes the edit capability when a page is a default view for a folder. [arsenico13]


0.2.0 (2016-12-09)
------------------

- Replaced unused plone.app.tiles.AddTile permission with "cmf.ModifyPortalContent"
  [cekk]
- Add Plone4 compatibility
  [cekk]
- Fix permission for add tile to "cmf.ModifyPortalContent"
  [arsenico13]
- Add italian translations
  [cekk]


0.1.0 (2016-09-19)
------------------

- Initial release.
  [cekk]
