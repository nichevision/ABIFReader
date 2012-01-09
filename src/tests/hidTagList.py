#!/usr/bin/env python
""" 
Represents a test of the ABIFReader for reading
.hid (human identification) files and listing the
contents within.
@author: Tom Faris
@email: ta.faris@gmail.com

"""
import sys,os
sys.path.append(os.path.realpath("../"))  # Append the '../src/' directory to our path so we can find the 'ABIF' module
from ABIF.ABIFReader import *

hidFile = "../../data/G04_7_IDP_500_19.hid"
hid = ABIFReader(hidFile)

print '****** ' + hid.file.name + ' ******'
hid.showEntries()