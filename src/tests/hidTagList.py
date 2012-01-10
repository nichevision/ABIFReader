#!C:\Python27\python.exe
""" 
Represents a test of the ABIFReader for reading
.hid (human identification) files and listing the
contents within.
@author: Tom Faris
@email: ta.faris@gmail.com

"""
import sys,os
from optparse import OptionParser
sys.path.append(os.path.realpath("../"))  # Append the '../src/' directory to our path so we can find the 'ABIF' module
from ABIF.ABIFReader import *

parser = OptionParser()
parser.add_option("-f", help="Filepath to the ABIF file.", dest="F");
(options,args) = parser.parse_args();

if not options.F:
	print "ABIF filepath must be specified."
else:
	hidFile = options.F
	hid = ABIFReader(hidFile)
	# First print all entries
	print '****** ' + hid.file.name + ' ******'
	hid.showEntries()

	# Now print the entries and their data
	for entry in hid.entries:
		print "************ Entry: %s ************" % (entry)
		data = hid.getData(entry.name,entry.number)
		if data:
			print data
		print ""
		print ""

	hid.close()