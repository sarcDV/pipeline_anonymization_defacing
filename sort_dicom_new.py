# Alex Weston
# Digital Innovation Lab, Mayo Clinic

import os, sys
import pydicom # pydicom is using the gdcm package for decompression

def clean_text(string):
    # clean and standardize text descriptions, which makes searching files easier
    forbidden_symbols = ["*", ".", ",", "\"", "\\", "/", "|", "[", "]", ":", ";", " "]
    for symbol in forbidden_symbols:
        string = string.replace(symbol, "_") # replace everything with an underscore
    return string.lower()  
   
# user specified parameters
# src = "test_1anom/"# "/home/m081739/projects/RSNA_temp/all_files"
# dst = "test_1sort/"# "/home/m081739/projects/RSNA_temp/sorted"

# Can run as a script:
if __name__ == "__main__":

    if len(sys.argv) != 3:
        print(usage)
        sys.exit()
    arg1, arg2 = sys.argv[1:]

    if os.path.isdir(arg1):
        src = arg1
        dst = arg2
        if os.path.exists(dst):
            if not os.path.isdir(dst):
                raise IOError("Input is directory; output name exists but is not a directory")
        else:  # out_dir does not exist; create it.
            os.makedirs(dst)

        # filenames = os.listdir(src)
        # for filename in filenames:
        #    if not os.path.isdir(os.path.join(src, filename)):
        #        # print(filename + "...", end='')
        #        print("done\r")
    else:  # first arg not a directory, assume two files given
        src = arg1
        dst = arg2
        

    print('reading file list...')
    unsortedList = []
    for root, dirs, files in os.walk(src):
        for file in files: 
            if "." in file:# exclude non-dicoms, good for messy folders  ".dcm"
                unsortedList.append(os.path.join(root, file))

    print('%s files found.' % len(unsortedList))
           
    for dicom_loc in unsortedList:
        # read the file
        ds = pydicom.read_file(dicom_loc, force=True)
       
        # get patient, study, and series information
        patientID = clean_text(ds.get("PatientID", "NA"))
        studyDate = clean_text(ds.get("StudyDate", "NA"))
        studyDescription = clean_text(ds.get("StudyDescription", "NA"))
        seriesDescription = clean_text(ds.get("SeriesDescription", "NA"))
       
        # generate new, standardized file name
        modality = ds.get("Modality","NA")
        studyInstanceUID = ds.get("StudyInstanceUID","NA")
        seriesInstanceUID = ds.get("SeriesInstanceUID","NA")
        instanceNumber = str(ds.get("InstanceNumber","0"))
        fileName = modality + "." + seriesInstanceUID + "." + instanceNumber + ".dcm"
           
        # uncompress files (using the gdcm package)
        try:
            ds.decompress()
        except:
            print('an instance in file %s - %s - %s - %s" could not be decompressed. exiting.' % (patientID, studyDate, studyDescription, seriesDescription ))
       
        # save files to a 4-tier nested folder structure
        if not os.path.exists(os.path.join(dst, patientID)):
            os.makedirs(os.path.join(dst, patientID))
       
        if not os.path.exists(os.path.join(dst, patientID, studyDate)):
            os.makedirs(os.path.join(dst, patientID, studyDate))
           
        if not os.path.exists(os.path.join(dst, patientID, studyDate, studyDescription)):
            os.makedirs(os.path.join(dst, patientID, studyDate, studyDescription))
           
        if not os.path.exists(os.path.join(dst, patientID, studyDate, studyDescription, seriesDescription)):
            os.makedirs(os.path.join(dst, patientID, studyDate, studyDescription, seriesDescription))
            print('Saving out file: %s - %s - %s - %s.' % (patientID, studyDate, studyDescription, seriesDescription ))
           
        ds.save_as(os.path.join(dst, patientID, studyDate, studyDescription, seriesDescription, fileName))

    print('done.')