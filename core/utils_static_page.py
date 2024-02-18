from bs4 import BeautifulSoup
from django.contrib.postgres.search import SearchVector


def refresh_searchable_static_page_bits(static_page, delete_only=False):
    # avoid circular imports
    from core.models import SearchableStaticPageBit

    # remove all SearchableStaticPageBits for this page
    SearchableStaticPageBit.objects.filter(static_page=static_page).delete()

    # when saving a static page and making it private,
    # don't create search vectors for its content
    if delete_only:
        return

    # extract text from content
    content_text = BeautifulSoup(static_page.content, "html.parser").get_text(
        " ", strip=True
    )

    # split into 2000 char chunks with 200 chars overlap
    for i in range(0, len(content_text), 1800):
        content_text_extract = content_text[i : i + 2000]

        # create the searchable static page bit
        new_searchable_page_bit = SearchableStaticPageBit(
            static_page=static_page, content_text_extract=content_text_extract
        )
        new_searchable_page_bit.save()

        # update the search vector
        # see https://stackoverflow.com/a/70812950
        new_searchable_page_bit.search_vector = SearchVector("content_text_extract")
        new_searchable_page_bit.save()
