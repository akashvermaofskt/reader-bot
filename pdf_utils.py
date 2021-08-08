import os
from pdf2image import convert_from_path
import PyPDF2
from dotenv import load_dotenv


def pdf_to_images(book_name, book_start_page):
    pages = convert_from_path(f"Books/{book_name}/{book_name}.pdf", 400)
    for page_no, page in enumerate(pages[book_start_page:]):
        print(f"Saving Page no. {page_no}")
        page.save(f"Books/{book_name}/PENDING/{page_no}.jpg", "JPEG")
        print(f"Done Page no. {page_no}")


def get_page_groups(
    book_name, book_start_page, reading_speed_wpm, reading_time_in_mins
):
    pdf = open(f"Books/{book_name}/{book_name}.pdf", "rb")
    pdf_reader = PyPDF2.PdfFileReader(pdf)
    print(" No. Of Pages :", pdf_reader.numPages)
    page_groups = []
    page_group = []
    count = 0
    for i in range(book_start_page, pdf_reader.numPages):
        page = pdf_reader.getPage(i)
        words = page.extractText().split()
        print(f"Page no. {(i-book_start_page)} has {len(words)}")
        count = count + len(words)
        page_group.append(i - book_start_page)
        if count >= (reading_speed_wpm * reading_time_in_mins):
            page_groups.append(page_group)
            page_group = []
            count = 0

    if len(page_group) > 0:
        page_groups.append(page_group)
        page_group = []
        count = 0

    print(page_groups)
    print(len(page_groups))
    return page_groups


if __name__ == "__main__":
    load_dotenv()
    BOOK_NAME = os.getenv("BOOK_NAME")
    BOOK_START_PAGE = int(os.getenv("BOOK_START_PAGE"))
    READING_SPEED_WPM = int(os.getenv("READING_SPEED_WPM"))
    READING_TIME_IN_MINS = int(os.getenv("READING_TIME_IN_MINS"))
    # get_page_groups(BOOK_NAME, BOOK_START_PAGE, READING_SPEED_WPM, READING_TIME_IN_MINS)
    pdf_to_images(BOOK_NAME, BOOK_START_PAGE)
