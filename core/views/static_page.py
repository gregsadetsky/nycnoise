from django.shortcuts import get_object_or_404, render

from ..models import StaticPage


def static_page(request, url_path):
    page_obj = get_object_or_404(StaticPage, url_path=url_path)
    return render(request, "core/static_page.html", {"page_obj": page_obj})
