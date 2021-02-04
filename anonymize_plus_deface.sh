#!/bin/bash
inputpatient=$1
newID=$2

mkdir "$newID"

python anonymize_newid.py "$inputpatient" "$newID" "$newID"

bash decompress_dicom.sh "$inputpatient"

python sort_dicom_new.py "$inputpatient" "$newID"/

bash convert_to_niigz.sh "$newID"

bash deface_new.sh "$newID" 

rm -rf "$inputpatient"/