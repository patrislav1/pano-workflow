#!/bin/bash

set -eux

SCRIPTDIR=$(dirname $(realpath $0))

PTODIR=${SCRIPTDIR}/tmp

pto_gen -o ${PTODIR}/nadir_reinsert.pto ${PTODIR}/zenit.tif ${PTODIR}/nadir.tif
pto_template --template=${SCRIPTDIR}/templates/nadir-reinsert.pto ${PTODIR}/nadir_reinsert.pto
pto_merge -o ${PTODIR}/merged.pto ${PTODIR}/nadir_reinsert.pto ${PTODIR}/pano_1stpass.pto
