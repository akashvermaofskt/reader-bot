from pdf2image import convert_from_path

pages = convert_from_path("Books/Drive/drive.pdf", 200)

page_no = 71
for page in pages[80:]:
    print(f"Saving Page no. {page_no}")
    page.save(f"Books/Drive/PENDING/{page_no}-out.jpg", "JPEG")
    print(f"Done Page no. {page_no}")
    page_no = page_no + 1
