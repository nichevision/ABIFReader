#!C:\Python27\python.exe
""" 
Represents a test of the HIDFileAlter for modifying a specified
HID file into a format that can be read by ABIFReader.
@author: Tom Faris
@email: ta.faris@gmail.com

"""

import sys,os
from optparse import OptionParser
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))  # Append the '../src/' directory to our path so we can find the 'ABIF' module
from ABIF.HIDFileAlter import *

# Setup an argument parser 
parser = OptionParser()
parser.add_option("-f", help="Filepath to the HID file to alter.", dest="F");
parser.add_option("-o", help="Filepath to where the modified HID file should be copied.", dest="O")
(options,args) = parser.parse_args();

if not options.F:
	print "HID filepath must be specified."
	exit(-1)
else:
	hidFileName = options.F
	
	if (not options.O): 
		# Create a destination file name since one was not specified
		alteredFileName = "MOD_%s" % (os.path.basename(os.path.realpath(hidFileName)))
	else:
		alteredFileName = options.O
	# Create an HIDFileAlter instance and alter the specified file
	fileAlter = HIDFileAlter(hidFileName)
	fileAlter.alterHIDFile(alteredFileName)