#!/bin/bash

set -eux

SCRIPTDIR=$(dirname $(realpath $0))

PTODIR=${SCRIPTDIR}/tmp

pano_modify --projection=0 --fov=90x90 --rotate=0,90,0 ${PTODIR}/pano_1stpass.pto -o ${PTODIR}/nadir.pto
pano_modify --projection=0 --fov=90x90 --rotate=0,-90,0 ${PTODIR}/pano_1stpass.pto -o ${PTODIR}/zenit.pto

hugin_executor --stitching ${PTODIR}/nadir.pto
mv ${PTODIR}/*-*.tif ${PTODIR}/nadir.tif
hugin_executor --stitching ${PTODIR}/zenit.pto
mv ${PTODIR}/*-*.tif ${PTODIR}/zenit.tif

