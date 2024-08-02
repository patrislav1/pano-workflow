#!/bin/bash

# Call script with first image of the series, it will then select a series of 8 consecutive images for the panorama

set -eux

SCRIPTDIR=$(dirname $(realpath $0))

FIRST_IMAGE=${1}

NUM_SCENES=8
NUM_EXP_PER_SHOT=3

IMGDIR=${SCRIPTDIR}/../img

# Function to extract the prefix, number and extension from a filename
extract_img_parts() {
    prefix=$(echo "$1" | sed -E 's/[0-9]+.*//')
    number=$(echo "$1" | grep -o -E '[0-9]+')
    extension=$(echo "$1" | sed -E 's/.*(\.[a-zA-Z0-9]+)$/\1/')
    echo "$prefix" "$number" "$extension"
}

mkdir -p ${IMGDIR}
rm -rf ${IMGDIR}/*.tif

# Extract filename numeric part, prefix, and extension
parts=($(extract_img_parts "$1"))
prefix=${parts[0]}
start_idx=${parts[1]}
start_idx=$((10#$start_idx)) # Remove leading zeros and prevent octal interpretation
extension=${parts[2]}

# Calculate the ending number
end_idx=$((start_idx + NUM_SCENES * NUM_EXP_PER_SHOT - 1))

seq_nbr=0
for img_start in $(seq $start_idx $NUM_EXP_PER_SHOT $end_idx); do
    file_list=""
    for img_exp in $(seq 0 $((NUM_EXP_PER_SHOT - 1))); do
	number=$(printf "%04d" $((img_start + img_exp)))
	file_name="${prefix}${number}${extension}"
	file_list+=" ${file_name}"
    done
    enfuse -o "${IMGDIR}/fused_$(printf "%04d" $seq_nbr).tif" ${file_list}
    seq_nbr=$((seq_nbr+1))
done

