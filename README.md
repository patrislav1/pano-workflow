# VR panorama workflow with Hugin, GIMP and [SLANT pano head](https://pt4pano.com/products/slant-nodalpunktadapter)

This is a set of scripts intended to build 360° x 180° panoramas shot in single-row technique with
a [SLANT panoramic head](https://pt4pano.com/products/slant-nodalpunktadapter).

The intention is to transform a set of photos into a
[equirectangular panorama](https://wiki.panotools.org/Equirectangular_Projection)
with as little user intervention as possible.

## Components

This repository is split into two parts:

* A script that uses the [Hugin CLI tools](https://wiki.panotools.org/Hugin#Hugin_components)
  to create a [Hugin](https://hugin.sourceforge.io/) project file

* A [GIMP](https://www.gimp.org/) plugin to automate the pre- and post-processing
  required for patching the zenith and nadir

## Requirements

* `bash` and `python3`

* The [Hugin suite](https://hugin.sourceforge.io/). The script should work with any recent version.
  It was tested with Hugin 2023.

* [GIMP](https://www.gimp.org/). The plugin requires a GIMP version with Python3 interface;
  at the time of writing this means installing the
  [2.99.x development version](https://z-uo.medium.com/create-python3-plugin-for-gimp-the-basics-94ede94e9d1f),
  that beta version is required until GIMP 3 is released.

  The beta version can be easily installed via flatpak:
  ```
  flatpak install --user https://flathub.org/beta-repo/appstream/org.gimp.GIMP.flatpakref
  ```

  * The GIMP step (zenith and nadir patching) is already possible with GIMP out of the box
    (see Filters -> Map -> Panorama Projection);
    the plugin only eliminates manual steps through automation.

  * To make GIMP aware of the plug-in, point it at the "gimp-plugin" folder in this repository:

    * Edit -> Preferences -> Folders -> Plug-ins

    * Add the path to the "gimp-plugin" directory

    * After restart, there should be a new menu entry (Filters -> Panorama)

# Usage

## Create panorama

* Call `create-pano.sh`, pointing it at the first photo of the series. It will select 8 consecutive image files for the panorama.

  e.g. `scripts/create-pano.sh /path/to/img/DSCF0025.JPG`

* The script creates a Hugin project containing the photo set, pre-aligns the photos
  (using known parameters like slant angle, lens properties, angle between images),
  creates control points and conducts a first optimization run.

* After the Hugin project is built it is opened in Hugin Panorama Creator GUI.

* Hugin GUI should already show a decent panorama; now it's possible to do some fine tuning
  (move/drag/straighten, further optimization etc)

* Select panorama format & resolution

* Finally stitch the panorama from the GUI or on the command line (e.g. `hugin_executor --stitching tmp/pano_final.pto`).

## Patch zenith & nadir

* Open the stiched panorama in GIMP.

* Run Filters -> Panorama -> Extract Zenith and Nadir
  * Two new layers should appear, containing the Zenith and Nadir in rectilinear projection.

* Patch the Zenith and Nadir layers until satisfied.

* Run Filters -> Panorama -> Reinsert Zenith and Nadir
  * The Zenith and Nadir layers should be reverted into equirectangular projection.

* The panorama can now be flattened & exported for further editing or publishing.

# Compatibility

The Hugin script was created for and tested with a Samyang 8mm f/2.8 Fisheye & Fuji X-E2
on a [PT4Pano SLANT pano head](https://pt4pano.com/products/slant-nodalpunktadapter).
This setup requires 8 single-row shots for a 360° x 180° panorama.

The script should work out of the box with any single-row fisheye setup using 8 shots for 360˚.

It should be easily adaptable for similar setups that use a different number of shots.

# TODO

* Support exposure bracketing for HDR panoramas.
* Use ML / GAN to "auto-patch" zenith and nadir without user intervention.

