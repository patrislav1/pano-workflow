#!/bin/bash

# Call script with first image of the series, it will then select a series of 8 consecutive images for the panorama

set -eu

SCRIPTDIR=$(dirname $(realpath $0))

FIRST_IMAGE=${1}

# Number of consecutive images to build the panorama from
NUM_IMAGES=8

# Uncomment if images are in clockwise rotation
COUNTERCLOCKWISE="--counterclockwise"

PTODIR=${SCRIPTDIR}/../tmp
PTOGENNAME=${PTODIR}/pano_generated.pto
PTOFINALNAME=${PTODIR}/pano_final.pto

# Lens values for Samyang 8mm f/2.8
# Full-frame fisheye
LENS_PROJ="3"
# Vertical field of view
LENS_FOV="155.5"

# Function to extract the prefix, number and extension from a filename
extract_img_parts() {
    prefix=$(echo "$1" | sed -E 's/[0-9]+.*//')
    number=$(echo "$1" | grep -o -E '[0-9]+')
    extension=$(echo "$1" | sed -E 's/.*(\.[a-zA-Z0-9]+)$/\1/')
    echo "$prefix" "$number" "$extension"
}

generate_pano() {
	# Create skeleton project with images
	pto_gen -o ${PTODIR}/pano_1.pto --projection=${LENS_PROJ} --fov=${LENS_FOV} ${@}

	# Set starting points for image positions
	${SCRIPTDIR}/set-angles.py ${PTODIR}/pano_1.pto -o ${PTODIR}/pano_2.pto ${COUNTERCLOCKWISE} --slant-angle 56

	# Set variables for optimization
	pto_var --opt="y,p,r,v,a,b,c,d,e,Vb,Vc,Vd,Ra,Rb,Rc,Rd,Re" -o ${PTODIR}/pano_3.pto ${PTODIR}/pano_2.pto

	# Add control points; work around cpfind 360° limitation by appending the first picture after the end
	${SCRIPTDIR}/img-append.py tmp/pano_3.pto tmp/pano_4.pto
	cpfind -o ${PTODIR}/pano_5.pto --celeste --linearmatch --fullscale ${PTODIR}/pano_4.pto
	${SCRIPTDIR}/img-remove.py tmp/pano_5.pto tmp/pano_6.pto

	# Clean up control points
	cpclean -o ${PTODIR}/pano_7.pto ${PTODIR}/pano_6.pto

	# Optimize image parameters to the control points; also set exposure values (aka photometry)
	autooptimiser -o ${PTODIR}/pano_8.pto -n -m ${PTODIR}/pano_7.pto

	# Clean up the control points once more
	cpclean -o ${PTOGENNAME} ${PTODIR}/pano_8.pto
}

# Extract filename numeric part, prefix, and extension
parts=($(extract_img_parts "$1"))
prefix=${parts[0]}
start_idx=${parts[1]}
start_idx=$((10#$start_idx)) # Remove leading zeros and prevent octal interpretation
extension=${parts[2]}

# Calculate the ending number
end_idx=$((start_idx + NUM_IMAGES - 1))

echo Generating panorama with:
file_list=""
for num in $(seq -f "%04g" $start_idx $end_idx); do
    file_name="${prefix}${num}${extension}"
    ls $file_name
    file_list+="${file_name} "
done

mkdir -p ${PTODIR}
rm -rf ${PTODIR}/*

LOGFILE=${PTODIR}/pano.log

echo Log file of panorama generation: ${LOGFILE}

generate_pano $file_list > ${LOGFILE} 2>&1

echo Done, generated panorama: ${PTOGENNAME}
echo Copying to ${PTOFINALNAME} and opening in hugin.

cp ${PTOGENNAME} ${PTOFINALNAME} && hugin ${PTOFINALNAME}

