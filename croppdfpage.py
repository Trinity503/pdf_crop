# -*- coding: utf-8 -*-
"""
This script splits scanned pdf pages with two actual pages gathered in one (horizontally).
It returns a single new pdf file with the split pages placed in correct order.
This can be usefull if you have pdf files of scanned old books and need to read them in an e-book reader like kindle.

"model page" is the one with the most frequent shape 
(setting it is important because many scanned books have the cover in distinct shape - usually portrait - than the rest of the book - usually landscape) 
 
Crops of different shapes can be made by changing the cropBox function parameters. 

Usage: yourpythonpath/python croppdfpage.py <pdffilename.pdf> <NEWpdffilename.pdf>

@author: Ana de Angelo - sanchesdeangelo@gmail.com
telegram: @anadeangelo
"""

import sys
from PyPDF2 import PdfWriter, PdfReader

file = str(sys.argv[1])
newfile = str(sys.argv[2])

with open(file, "rb") as pdf1:
    pdf = PdfReader(pdf1)
    output = PdfWriter()
    page1 =  pdf.pages[int(input('insert the number of the model page: '))]
    ll_x = page1.trimbox.lower_left[0]  #ll stands for lower left
    ll_y = page1.trimbox.lower_left[1]
    ur_x = page1.trimbox.upper_right[0] #ur stands for upper right
    ur_y = page1.trimbox.upper_right[1]
	
    numpages = len(pdf.pages)

    for i in range(numpages):
        page = pdf.pages[i]
        if i == 0: #cover is last_side_first_side
            page.cropbox.lower_left = ((ur_x/2)+5, ll_y)
            page.cropbox.upper_right = (ur_x, ur_y)
            output.add_page(page)
        else:        
            page.cropbox.lower_left = (ll_x, ll_y)
            page.cropbox.upper_right = ((ur_x/2)-5, ur_y)
            output.add_page(page)
        #else:
            page.cropbox.lower_left = ((ur_x/2)+5, ll_y)
            page.cropbox.upper_right = (ur_x, ur_y)
            output.add_page(page)
    
    page = pdf.pages[0] #create back cover page
    page.cropbox.lower_left = (ll_x, ll_y)
    page.cropbox.upper_right = ((ur_x/2)-5, ur_y)
    output.add_page(page)
        
    with open(newfile, "wb") as newpdf:
        output.write(newpdf)