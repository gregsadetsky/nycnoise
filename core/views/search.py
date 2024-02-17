from django.contrib.postgres.search import SearchVector
from django.shortcuts import render

from ..models import Event, SearchableStaticPageBit, StaticPage


def search(request):
    query = request.GET.get("s", "").strip()

    # full text, case insensitive search on static page content
    if not query:
        return render(request, "core/search.html")

    # get all static page objects
    found_static_page_ids = (
        SearchableStaticPageBit.objects.annotate(
            search=SearchVector("content_text_extract")
        )
        .filter(search=query)
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
