from time import sleep
from xml2epub import Epub, create_chapter_from_string  # Import the necessary classes
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_html(url):
    brave_path = "/usr/bin/brave"  # Update this path if necessary
    chrome_options = Options()
    chrome_options.binary_location = brave_path

    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)
        content_section = (By.ID, "reader-container")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(content_section))

        content_element = driver.find_element(By.ID, "reader-container")
        final_html = content_element.get_attribute("outerHTML")
        return final_html
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None
    finally:
        driver.quit()


def make_chapter(url):
    html = get_html(url)
    if html is None:
        return None
    # title is the last part of the URL after the last '/'
    title = url.split("/")[-1].replace("-", " ").title()
    return create_chapter_from_string(html, url, title=title)


def add_chapter(book, url):
    chapter = make_chapter(url)
    if chapter is not None:
        book.add_chapter(chapter)


# Example Usage: Replace with the URL you want to convert
original_url = "https://wetriedtls.com/series/a-regressors-tale-of-cultivation/chapter-"

# starts from 364 until 731. Make books of 25 chapters each
all_chapters = list(range(364, 732))
for i in tqdm(range(0, len(all_chapters), 25)):
    epub = Epub(
        f"A Regressor's Tale of Cultivation - Chapters {all_chapters[i]} to {all_chapters[i + 24]}",
    )
    for j in range(i, min(i + 25, len(all_chapters))):
        chapter_url = f"{original_url}{all_chapters[j]}"
        add_chapter(epub, chapter_url)
        sleep(3)  # Be polite and avoid overwhelming the server

    epub.create_epub("epub_saved/")
