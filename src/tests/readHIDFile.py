#!C:\Python27\python.exe
""" 
Combines the functionality of the modHIDFile.py script and
the ABIFTagList.py script to make it more simple to convert
and extract data from an HID file.
@author: Tom Faris
@email: ta.faris@gmail.com

"""

import subprocess,os,re
from optparse import OptionParser

# Read cmd line arguments
parser = OptionParser()
parser.add_option("-f", help="Filepath to the HID file.", dest="F");
(options,args) = parser.parse_args();

if not options.F:
	print "HID filepath must be specified."
else:
	inputFilePath = options.F
	# Create a new name for the modified HID file to output to
	outputFilePath = "MOD_%s" % (os.path.basename(os.path.realpath(inputFilePath)))
	# Create the modified HID file by calling the modHIDFile.py script, passing it the input and output file paths
	subprocess.call(["python", "modHIDFile.py", "-f%s" % (inputFilePath), "-o%s" % outputFilePath])
	# Create the xml tag list by calling the ABIFTagList.py script, passing it the file path to the modified HID file
	p = subprocess.Popen(["python", "ABIFTagList.py", "-f%s" % outputFilePath], stdout=subprocess.PIPE)
	# Capture process output
	out, err = p.communicate()
	# "out" is the stdout text from running the script above
	# Create a file to recieve the output
	splitPath = os.path.splitext(os.path.basename(outputFilePath))
	outputXmlPath = "%s.xml" % (splitPath[len(splitPath)-2])
	# When we read the xml from stdout there are extra lines inserted. Remove them with this regular expression.
	prettyPrintNewLineRegex = re.compile(r'((?<=>)(\n[\t]*)(?=[^<\t]))|(?<=[^>\t])(\n[\t]*)(?=<)')
	prettyXml = re.sub(prettyPrintNewLineRegex, '', out)
	# Save out to the xml file
	print "Creating XML output in %s..." % outputXmlPath
	xmlFileOut = open(outputXmlPath, "w+")
	xmlFileOut.write(prettyXml)
	xmlFileOut.close()