import requests
from xml2epub import Epub, Chapter  # Import the necessary classes


def convert_whole_page_to_epub(url):
    """Fetches the full HTML and converts it directly to a single-chapter EPUB."""
    try:
        # 1. Fetch the entire HTML content
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        full_html_content = response.text

        # 2. Initialize the EPUB
        get_last_segment = url.rstrip("/").split("/")[-1]
        epub = Epub(title=get_last_segment, creator="Automated Scraper")

        # 3. Create a single chapter from the full HTML string
        # The title can be the original <title> tag text
        page_title = (
            full_html_content.split("<title>")[1].split("</title>")[0]
            if "<title>" in full_html_content
            else "Web Page"
        )

        main_chapter = Chapter(
            title=page_title,
            html_content=full_html_content,
            # We don't want xml2epub's default cleaning, so we set strict=False
            # to include everything, including scripts and styles (though EPUB validation might flag it)
            strict=False,
        )

        epub.add_chapter(main_chapter)

        # 4. Save the EPUB file
        output_filename = f"./epubs_saved/{get_last_segment}.epub"
        epub.create_epub(output_filename)
        print(f"✅ Success! EPUB file saved as: {output_filename}")

    except Exception as e:
        print(f"❌ An error occurred: {e}")


# Example Usage: Replace with the URL you want to convert
# convert_whole_page_to_epub("https://en.wikipedia.org/wiki/Arch_Linux")
original_url = "https://wetriedtls.com/series/a-regressors-tale-of-cultivation/chapter-"
all_chapters = [364]
for chapter_num in all_chapters:
    chapter_url = f"{original_url}{chapter_num}"
    convert_whole_page_to_epub(chapter_url)
