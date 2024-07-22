# VR panorama workflow with Hugin and [PT4Pano SLANT adapter](https://pt4pano.com/products/slant-nodalpunktadapter)

## Create panorama

* Make new hugin project, add photos

* Apply SLANT template (`template.pto`)

* Optimize control points (positions, view and barrel)

* Optimize photometric (High dynamic range)

* Set stitcher to low dynamic range, enblend

* Tweak pano until good, Move/straighten/etc.

* Save to pano.pto

## Patch zenit & nadir

* Create zenit/nadir rectilinear images

  ```bash
  pano_modify --projection=0 --fov=90x90 --rotate=0,90,0 pano.pto -o nadir.pto
  pano_modify --projection=0 --fov=90x90 --rotate=0,-90,0 pano.pto -o zenit.pto
  hugin_executor --stitching nadir.pto
  mv *-*.tif nadir.tif
  hugin_executor --stitching zenit.pto
  mv *-*.tif zenit.tif
  ```

* Patch zenit / nadir
  * IMPORTANT: when exporting from GIMP, deselect "layers" and "color profile" in TIF options
  
* Open pano project in Hugin
  * Add zenit / nadir images with settings: rectilinear & 90deg FOV
  * Set zenit to 90deg pitch and nadir to -90deg pitch
  * Add include mask to nadir (hide the tripod)

* Re-do photometric optimization

* Stitch main panorama

  ```bash
  hugin_executor --stitching pano.pto
  ```

