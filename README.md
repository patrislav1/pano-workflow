# VR panorama workflow with Hugin, GIMP and [SLANT pano head](https://pt4pano.com/products/slant-nodalpunktadapter)

This is a set of scripts intended to build 360° x 180° panoramas shot in single-row technique with
a [SLANT panoramic head](https://pt4pano.com/products/slant-nodalpunktadapter).

The intention is to transform a set of photos into a
[equirectangular panorama](https://wiki.panotools.org/Equirectangular_Projection)
with as little user intervention as possible.

## Components

This repository is split into 2 parts:

1) a script that uses the [Hugin CLI tools](https://wiki.panotools.org/Hugin#Hugin_components)
   to create a [Hugin](https://hugin.sourceforge.io/) project file

2) a [GIMP](https://www.gimp.org/) plugin to automate the pre- and post-processing for patching the zenith and nadir

## Requirements

* The Hugin script should work with any recent version of the Hugin suite. It was tested with Hugin 2023.

* The GIMP plugin requires a GIMP version with Python3 interface; at the time of writing this means installing
  the [2.99.x development version](https://z-uo.medium.com/create-python3-plugin-for-gimp-the-basics-94ede94e9d1f),
  that beta version is required until GIMP 3 is released.

  The beta version can be easily installed via flatpak:
  ```
  flatpak install --user https://flathub.org/beta-repo/appstream/org.gimp.GIMP.flatpakref
  ```

* `bash` and `python3`

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

## Patch zenit & nadir

TODO
