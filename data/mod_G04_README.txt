The file "mod_G04_7_IDP_500_19.hid" was created using the following steps:

1) Create a copy of "G04_7_IDP_500_19.hid"
2) Open the copy in a hex editor
3) Find the byte-offset of the first occurence of the first tag in the list of entries for "G04_7_IDP_500_19.hid" (get the entries using ABIFReader.py).
4) Set the dataoffset property of the "tdir" directory element of the open file to the byte-offset from above.
   The dataoffset property should be represented by the 4-byte block 1A-1D (26-29). It is the offset of the "tdir" element plus 20 bytes.
5) Save the file.