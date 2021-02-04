#!/bin/bash

inputfolder=$1	
for d in "$inputfolder"/defaced_anony_nii/*; 
do
    echo "$d"
	cd "$d"/
	ls
	for fullfile in *.nii.gz;
	do 	
		info_=`fslinfo "$fullfile"`
		dim1_=`echo $info_ | cut -d' ' -f4`
		dim2_=`echo $info_ | cut -d' ' -f6`
		dim3_=`echo $info_ | cut -d' ' -f8`
		dim4_=`echo $info_ | cut -d' ' -f10`

		res1_=`echo $info_ | cut -d' ' -f14`
		res2_=`echo $info_ | cut -d' ' -f16`
		res3_=`echo $info_ | cut -d' ' -f18`


		if [[ "$dim3_" -le 5 ]]; then
			echo "                                "
			echo "... one slice or few slices only ..."
			echo "... not processing: " "$fullfile"
			echo "$dim1_" "$dim2_" "$dim3_" "$res1_" "$res2_" "$res3_"
		else
			filename=$(basename -- "$fullfile")
			extension="${filename##*.}"
			filename="${filename%.*.*}"
				
			if [[ "$filename" == *"DW"*  ||  "$filename" == *"T2"* ||  "$filename" == *"DTI"* ||  "$filename" == *"T1"* ]]  ; then
				echo "                                "
			  	echo "... processing... ""$filename";
			  	echo "$dim1_" "$dim2_" "$dim3_" "$res1_" "$res2_" "$res3_"
				bet2 "$filename".nii.gz brain.nii.gz -f 0.15
				fslmaths "$filename".nii.gz -sub brain.nii.gz skull.nii.gz
				fslmaths skull.nii.gz -dilF dilF-skull.nii.gz
				fslmaths dilF-skull.nii.gz -s 5 smoothed-dilF-skull.nii.gz 
				fslmaths brain.nii.gz -binv brain-mask.nii.gz
				fslmaths brain-mask.nii.gz -mul smoothed-dilF-skull.nii.gz smoothed-dilF-skull.nii.gz
				fslmaths brain.nii.gz -add smoothed-dilF-skull.nii.gz defaced-"$filename".nii.gz
				rm -rf brain.nii.gz brain-mask.nii.gz smoothed-dilF-skull.nii.gz dilF-skull.nii.gz skull.nii.gz
			else
				echo "                                "
				echo "... processing... ""$filename";
				mri_watershed "$filename".nii.gz brain.nii.gz
				fslmaths "$filename".nii.gz -sub brain.nii.gz skull.nii.gz
				fslmaths skull.nii.gz -dilF dilF-skull.nii.gz
				fslmaths dilF-skull.nii.gz -s 5 smoothed-dilF-skull.nii.gz 
				fslmaths brain.nii.gz -binv brain-mask.nii.gz
				fslmaths brain-mask.nii.gz -mul smoothed-dilF-skull.nii.gz smoothed-dilF-skull.nii.gz
				fslmaths brain.nii.gz -add smoothed-dilF-skull.nii.gz defaced-"$filename".nii.gz
				rm -rf brain.nii.gz brain-mask.nii.gz smoothed-dilF-skull.nii.gz dilF-skull.nii.gz skull.nii.gz
			fi
		fi

	done
	cd ../../../
done



