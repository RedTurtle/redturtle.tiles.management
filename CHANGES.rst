Changelog
=========


0.3.1 (unreleased)
------------------

- Nothing changed yet.


0.3.0 (2019-12-02)
------------------

- Store tiles_list into a PersistentList to persist order between instances and restarts.
  [cekk]


0.2.2 (2018-10-12)
------------------

- Tiles no more need to expose tile_id. Now is handled in the template.
  [cekk]
- Fix integration.js code
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
