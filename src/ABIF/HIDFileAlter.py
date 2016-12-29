#!C:\Python27\python.exe
#
# HID files (as of 01/2012) do not work right out of the box with the ABIFReader script.
# The problem is that the "tdir" root directory element of the ABIF file format seems to 
# point to the wrong byte offset (via its "dataoffset" property) in the file for the rest 
# of its entries. However, the HID file actually contains more than one listing of directory 
# entries. Some seem to contain 2-3. By replacing the existing value for tdir.dataoffset 
# with the offset of the first listing of these entries, we are able to read the file using
# ABIFReader with no issue.
#
# This script takes a specified HID file, locates the first listing of directory entries,
# copies the file and replaces the existing tdir offset with the located offset, thus making
# it readable with ABIFReader.
#
import sys,os,shutil
from ABIFReader import *

class HIDFileAlter:
    """A simple class that can be used to alter files of the HID type (*.hid) so that they can be read using ABIF.ABIFReader.
@author: Tom Faris
    """
    def __init__(self,fileName):    
        # Defines the byte offset into the HID file where that represents
        # an integer that is used to locate the rest of the directory elements.
        self.__TDIR_DATAOFFSET_BYTE_POS = 26    
        self.hidFile = fileName;
    
    def alterHIDFile(self, fileName):
        """alterHIDFile(fileName) -> None. Alters the file specified in the constructor and saves it to the specified fileName."""
        self.alteredFileName = fileName;
        # Read the original HID file
        self.hid = ABIFReader(self.hidFile)
        # Get the first directory entry of the original file
        firstEntry = self.hid.entries[0]
        # Set the file seek position to 0
        self.hid.seek(0)
        # Read the entire file into a string buffer -- this method can probably be optimized
        bytes = self.hid.file.read()
        # Find the first string index of the name of the first tag in our file.
        # This correspond to the byte offset of the entry. 
        index = bytes.find(firstEntry.name);

        if index >= 0:
            print "Current byte offset is %s. New byte offset will be %s" % (firstEntry.mydataoffset(), index)
            # Pack the new index into a buffer as a big-endian integer
            correctOffset = struct.pack(">i", index)
            # Create a name for the modified file
            #copyFileName = os.path.dirname(os.path.realpath(self.hidFile)) + "%sMOD_%s" % (os.sep, os.path.basename(os.path.realpath(self.hidFile)))
            sys.stdout.write("Creating modified file %s..." % self.alteredFileName)
            # Copy the original file to the new file name
            shutil.copy2(self.hidFile,self.alteredFileName)
            # Open the new file
            copyFile = open(self.alteredFileName, 'r+')
            # Seek to the byte offset that represents the dataoffset for the TDIR directory element.
            copyFile.seek(self.__TDIR_DATAOFFSET_BYTE_POS)
            # Write the new offset to the file and close
            copyFile.write(correctOffset)
            copyFile.close()
            sys.stdout.write("done.%s" % os.linesep);
            
            print "*********************"
            copyHID = ABIFReader(self.alteredFileName)
            copyEntries = copyHID.entries
            originalEntries = self.hid.entries
            print "Original # of directory entries is %i. New # of directory entries is %i. (Should be equal.)" % (len(originalEntries), len(copyEntries))
            copyHID.close()
        else:
            print "Could not find an index for the first entry \"%s\"." % (firstEntry.name)
            
        self.hid.close()