# VR panorama workflow with Hugin and [PT4Pano SLANT adapter](https://pt4pano.com/products/slant-nodalpunktadapter)

## Create panorama

* Call `pano-init.sh`, pointing it at the first image of the series. It will select 8 consecutive image files for the panorama.

e.g.

```bash
$ ./pano-init.sh ~/Pictures/RAW/slant-test/DSCF0025.JPG
Generating panorama with:
/home/patrick/Pictures/RAW/slant-test/DSCF0025.JPG
/home/patrick/Pictures/RAW/slant-test/DSCF0026.JPG
/home/patrick/Pictures/RAW/slant-test/DSCF0027.JPG
/home/patrick/Pictures/RAW/slant-test/DSCF0028.JPG
/home/patrick/Pictures/RAW/slant-test/DSCF0029.JPG
/home/patrick/Pictures/RAW/slant-test/DSCF0030.JPG
/home/patrick/Pictures/RAW/slant-test/DSCF0031.JPG
/home/patrick/Pictures/RAW/slant-test/DSCF0032.JPG
Log file of panorama generation: /home/patrick/src/pano-workflow/tmp/pano.log
Done, generated panorama: /home/patrick/src/pano-workflow/tmp/pano_generated.pto
Copying to /home/patrick/src/pano-workflow/tmp/pano_final.pto and opening in hugin.
```

## Patch zenit & nadir

TODO
