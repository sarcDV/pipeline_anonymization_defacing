The main file is "anonymize_plus_deface.sh". 

It takes two arguments as input: 
    a) input folder, the original data
    b) the new ID assigned by another script

It contains a series of python and bash scripts:

 1) python anonymize_newid.py "$inputpatient" "$newID" "$newID"

 2) bash decompress_dicom.sh "$inputpatient"

 3) python sort_dicom_new.py "$inputpatient" "$newID"/

 4) bash convert_to_niigz.sh "$newID"

 5) bash deface_new.sh "$newID" 


## step 1:


anonymize dicom files with anonymize_newid.py (python script, dependencies: os, sys, pydicom ):

usage: python anonymize_newid.py "input-folder" "output-folder" new-id


## step 2:

uncompress anonymized dicom files with  decompress_dicom.sh (bash script, dependencies: "gdcmconv"  ): 

usage:  bash decompress_dicom.sh "input-folder"


## step 3 

sort dicom files with sort_dicom_new.py  (python script, dependencies: os, sys, pydicom ):

usage:  python sort_dicom_new.py "input-folder" "output-folder"

## step 4

convert to nii format with dcn2niix (bash script, dependencies: "dcm2nii"  ): 

bash convert_to_niigz.sh

## step 5

deface, replace the skull:

bash deface_new.sh

## step 6

remove/delete the original folder
