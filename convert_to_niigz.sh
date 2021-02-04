#!/bin/bash

## find test_1sort/ -type d -links 2

newID=$1

for d in "$newID"/*/*/*/*/; 
do
    # echo "$d"
    dcm2niix -o "$d" -z y "$d"
done




cd "$newID"/
mkdir defaced_anony_nii
mkdir compressed_anony_dicom
mv *.*.*.* compressed_anony_dicom/

## delete dicom
find . -maxdepth 5 -mindepth 5 -type f -name '*.*.*.*' -exec rm -rf {} \;

## move nii file to anony_nii
find . -maxdepth 4 -mindepth 4 -type d -exec mv {} defaced_anony_nii/ \;

## delete empty folders
find . -type d -empty -print
find . -type d -empty -delete




