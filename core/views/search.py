from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import F
from django.shortcuts import render

from ..models import Event, SearchableStaticPageBit, StaticPage


def search(request):
    query = request.GET.get("s", "").strip()

    # full text, case insensitive search on static page content
    if not query:
        return render(request, "core/search.html")

    # https://stackoverflow.com/a/70812950
    search_query = SearchQuery(query, search_type="websearch", config="english")
    search_rank = SearchRank(F("search_vector"), search_query)
    found_static_page_ids = (
        SearchableStaticPageBit.objects.annotate(rank=search_rank)
        .filter(search_vector=search_query)  # Perform full text search on index.
        .values("static_page__id")
        .distinct()
    )
    results_pages = (
        StaticPage.objects.filter(id__in=found_static_page_ids).order_by("title").all()
    )

    results_events = (
        Event.objects.annotate(
            search=SearchVector(
                "title",
                "artists",
                "venue__name",
                "venue_override",
                "description",
                "preface",
            )
        )
        .filter(search=query)
        .order_by("starttime")
        .distinct()
        .all()
    )

    return render(
        request,
        "core/search.html",
        {
            "query": query,
            "results_pages": results_pages,
            "results_events": results_events,
        },
    )
