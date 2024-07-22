#!/bin/bash

set -eux

SCRIPTDIR=$(dirname $(realpath $0))

PTODIR=${SCRIPTDIR}/tmp
mkdir -p ${PTODIR}
rm -rf ${PTODIR}/*

pto_gen -o ${PTODIR}/pano_img.pto ${1}/*
pto_template -o ${PTODIR}/pano_templ.pto --template=${SCRIPTDIR}/templates/templ-slant-8exp.pto ${PTODIR}/pano_img.pto
cpfind -o ${PTODIR}/pano_cp.pto --celeste --prealigned --fullscale ${PTODIR}/pano_templ.pto
cpclean -o ${PTODIR}/pano_clean.pto ${PTODIR}/pano_cp.pto
autooptimiser -o ${PTODIR}/pano_opt.pto -n ${PTODIR}/pano_clean.pto
cpclean -o ${PTODIR}/pano_1stpass.pto ${PTODIR}/pano_opt.pto

