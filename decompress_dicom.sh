#!/bin/bash
inputfolder=$1	

echo "... uncompressing ... " "$inputfolder"		
for files in "$inputfolder"/*;
do 
	gdcmconv -w "${files}"  "${files}"
done
echo "... done!!!" 