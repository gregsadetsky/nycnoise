from bs4 import BeautifulSoup


def refresh_searchable_static_page_bits(static_page):
    # avoid circular imports
    from core.models import SearchableStaticPageBit

    # remove all SearchableStaticPageBits for this page
    SearchableStaticPageBit.objects.filter(static_page=static_page).delete()

    # extract text from content
    content_text = BeautifulSoup(static_page.content, "html.parser").get_text(
        " ", strip=True
    )

    # split into 2000 char chunks with 200 chars overlap
    for i in range(0, len(content_text), 1800):
        content_text_extract = content_text[i : i + 2000]
        SearchableStaticPageBit.objects.create(
            static_page=static_page, content_text_extract=content_text_extract
        )
