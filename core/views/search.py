from django.contrib.postgres.search import SearchVector
from django.shortcuts import render

from ..models import Event, StaticPage


def search(request):
    query = request.GET.get("s", "").strip()

    # full text, case insensitive search on static page content
    if not query:
        return render(request, "core/search.html", {"query": query})

    results_pages = (
        StaticPage.objects.annotate(search=SearchVector("title", "content"))
        .filter(search=query)
        .order_by("title")
        .distinct()
        .all()
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
