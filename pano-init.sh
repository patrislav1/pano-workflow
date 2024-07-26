#!/bin/bash

# Call script with first image of the series, it will then select a series of 8 consecutive images for the panorama

set -eu

SCRIPTDIR=$(dirname $(realpath $0))

FIRSTIMAGE=${1}

PTODIR=${SCRIPTDIR}/tmp
PTOGENNAME=${PTODIR}/pano_generated.pto
PTOFINALNAME=${PTODIR}/pano_final.pto

# Function to extract the prefix, number and extension from a filename
extract_img_parts() {
    prefix=$(echo "$1" | sed -E 's/[0-9]+.*//')
    number=$(echo "$1" | grep -o -E '[0-9]+')
    extension=$(echo "$1" | sed -E 's/.*(\.[a-zA-Z0-9]+)$/\1/')
    echo "$prefix" "$number" "$extension"
}

generate_pano() {
	# Create skeleton project with images
	pto_gen -o ${PTODIR}/pano_1.pto ${@}

	# Apply template with starting points for image positions / lens data
	pto_template -o ${PTODIR}/pano_2.pto --template=${SCRIPTDIR}/templates/templ-slant-8exp.pto ${PTODIR}/pano_1.pto

	# Add control points; work around cpfind 360° limitation by appending the first picture after the end
	${SCRIPTDIR}/img-append.py tmp/pano_2.pto tmp/pano_3.pto
	cpfind -o ${PTODIR}/pano_4.pto --celeste --linearmatch --fullscale ${PTODIR}/pano_3.pto
	${SCRIPTDIR}/img-remove.py tmp/pano_4.pto tmp/pano_5.pto

	# Clean up control points
	cpclean -o ${PTODIR}/pano_6.pto ${PTODIR}/pano_5.pto

	# Optimize image parameters to the control points; also set exposure values (aka photometry)
	autooptimiser -o ${PTODIR}/pano_7.pto -n -m ${PTODIR}/pano_6.pto

	# Clean up the control points once more
	cpclean -o ${PTOGENNAME} ${PTODIR}/pano_7.pto
}

# Number of consecutive images to build the panorama from
num_imgs=8

# Extract numeric part, prefix, and extension
parts=($(extract_img_parts "$1"))
prefix=${parts[0]}
start_idx=${parts[1]}
start_idx=$((10#$start_idx)) # Remove leading zeros and prevent octal interpretation
extension=${parts[2]}

# Calculate the ending number
end_idx=$((start_idx + num_imgs - 1))

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

