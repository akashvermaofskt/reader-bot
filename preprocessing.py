# extracting each page as an image and saving it to separate folder
import os
import shutil

from pdf2image import convert_from_path
pages = convert_from_path('books/pdf/SamplePdf.pdf', 500, output_folder='books/output_folder/')

# saving images in png format
total_pages = 0
for i, page in enumerate(pages):
    pname = 'page' + str(i) + '.png'
    page.save(pname, 'PNG')
    total_pages = max(i, total_pages)

# now move each file to 'pending' folder
source = 'D:/Dev/reader-bot/page'
destination = 'D:/Dev/reader-bot/books/pending/'

for i in range(total_pages):
    tempSource = source + str(i) + '.png'
    dest = shutil.move(tempSource, destination)