from __future__ import print_function

usage = """
Usage:
python anonymize.py dicomfile.dcm outputfile.dcm
OR
python anonymize.py originals_directory anonymized_directory

Note: Use at your own risk. Does not fully de-identify the DICOM data as per
the DICOM standard, e.g in Annex E of PS3.15-2011.
"""

import os
import os.path
import pydicom


def anonymize_newid(filename, output_filename, # new_person_name="anonymous",
              new_patient_id, remove_curves=True, remove_private_tags=True):
    """Replace data element values to partly anonymize a DICOM file.
    Note: completely anonymizing a DICOM file is very complicated; there
    are many things this example code does not address. USE AT YOUR OWN RISK.
    """

    # Define call-back functions for the dataset.walk() function
    def PN_callback(ds, data_element):
        """Called from the dataset "walk" recursive function for all data elements."""
        if data_element.VR == "PN":
            data_element.value = new_patient_id # new_person_name

    def curves_callback(ds, data_element):
        """Called from the dataset "walk" recursive function for all data elements."""
        if data_element.tag.group & 0xFF00 == 0x5000:
            del ds[data_element.tag]

    # Load the current dicom file to 'anonymize'
    dataset = pydicom.read_file(filename)

    # Remove patient name and any other person names
    dataset.walk(PN_callback)

    # Change ID
    dataset.PatientID = new_patient_id

    # Remove data elements (should only do so if DICOM type 3 optional)
    # Use general loop so easy to add more later
    # Could also have done: del ds.OtherPatientIDs, etc.
    for name in ['OtherPatientIDs', 'OtherPatientIDsSequence']:
        if name in dataset:
            delattr(dataset, name)

    # Same as above but for blanking data elements that are type 2.
    for name in ['PatientBirthDate']:
        if name in dataset:
            dataset.data_element(name).value = ''

    # Remove private tags if function argument says to do so. Same for curves
    if remove_private_tags:
        dataset.remove_private_tags()
    if remove_curves:
        dataset.walk(curves_callback)

    # write the 'anonymized' DICOM out under the new filename
    dataset.save_as(output_filename)

# Can run as a script:
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4: # 3:
        print(usage)
        sys.exit()
    arg1, arg2, arg3 = sys.argv[1:]

    if os.path.isdir(arg1):
        in_dir = arg1
        out_dir = arg2
        new_id = arg3
        if os.path.exists(out_dir):
            if not os.path.isdir(out_dir):
                raise IOError("Input is directory; output name exists but is not a directory")
        else:  # out_dir does not exist; create it.
            os.makedirs(out_dir)

        filenames = os.listdir(in_dir)
        for filename in filenames:
            if not os.path.isdir(os.path.join(in_dir, filename)):
                print(filename + "...", end='')
                anonymize_newid(os.path.join(in_dir, filename), os.path.join(out_dir, filename), new_patient_id=new_id)
                print("done\r")
    else:  # first arg not a directory, assume two files given
        in_filename = arg1
        out_filename = arg2
        new_id = arg3
        anonymize_newid(in_filename, out_filename, new_patient_id=new_id)
    print()
