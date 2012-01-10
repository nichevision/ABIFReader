#!C:\Python27\python.exe
""" 
Represents a test of the ABIFReader for reading
ABIF-formatted files and listing the contents within.
@author: Tom Faris
@email: ta.faris@gmail.com

"""
import sys,os,re
from optparse import OptionParser
from xml.dom.minidom import Document
from time import gmtime, strftime
sys.path.append(os.path.realpath("../"))  # Append the '../src/' directory to our path so we can find the 'ABIF' module
from ABIF.ABIFReader import *

def appendTextNode(doc, nodeToAppendTo, newElementName, data):
	newNode = doc.createElement(newElementName)
	if type(data) is int or type(data) is long:
		dataString = "%i" % data
	elif type(data) is float:
		dataString = "%f" % data
	elif data == "\x00":
		dataString = "0"
	elif data == "\x01":
		dataString = "1"
	else:
		dataString = "%s" % data
	newNode.appendChild(doc.createTextNode(dataString))
	nodeToAppendTo.appendChild(newNode)

# Read cmd line arguments
parser = OptionParser()
parser.add_option("-f", help="Filepath to the ABIF file.", dest="F");
(options,args) = parser.parse_args();

if not options.F:
	print "ABIF filepath must be specified."
else:
	abifFile = options.F
	abi = ABIFReader(abifFile)
	# Create an XML document
	doc = Document()
	# Create root element
	root = doc.createElement("AB_Root")
	doc.appendChild(root)
	# Create properties element
	props = doc.createElement("Properties")
	root.appendChild(props)
	appendTextNode(doc,props, "Creator", "NicheVision ABIFTagList 1.0")
	appendTextNode(doc,props,"Date_Created",strftime("%Y-%m-%d %H:%M:%S", gmtime()))
	appendTextNode(doc,props,"Data_Source", abifFile)
	# Create header element
	header = doc.createElement("Header")
	root.appendChild(header)
	appendTextNode(doc,header,"Version",abi.version)
	appendTextNode(doc,header,"ByteOrder",abi.type)
	appendTextNode(doc,header,"Directory_Tag_Name",abi.rootEntry.name)
	appendTextNode(doc,header,"Directory_Elements",len(abi.entries))
	#Create data (tag) elements
	dataRoot = doc.createElement("Data")
	root.appendChild(dataRoot)
	for entry in abi.entries:
		tag = doc.createElement("Tag")
		dataRoot.appendChild(tag)
		appendTextNode(doc,tag,"Name",entry.name)
		appendTextNode(doc,tag,"ID",entry.number)
		appendTextNode(doc,tag,"Type",entry.mytype())
		appendTextNode(doc,tag,"Elements",entry.numelements)
		appendTextNode(doc,tag,"ElementSize",entry.elementsize)
		appendTextNode(doc,tag,"ElementType",entry.elementtype)
		appendTextNode(doc,tag,"DataSize",entry.datasize)
		data = abi.getData(entry.name,entry.number)
		appendTextNode(doc,tag,"Value",data)
	
	prettyXml = doc.toprettyxml(indent="\t")
	# Document.toprettyxml inserts newlines after each element... this regex strips out the extra whitespace.
	# This is unnecessary, but looksa  whole lot better!
	prettyPrintNewLineRegex = re.compile(r'((?<=>)(\n[\t]*)(?=[^<\t]))|(?<=[^>\t])(\n[\t]*)(?=<)')
	prettyXml = re.sub(prettyPrintNewLineRegex, '', prettyXml)
	print prettyXml
	# Cleanup
	abi.close()
