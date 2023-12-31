from core.sitemap import SiteSitemap
from core.views.static_page import static_page
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path

urlpatterns = [
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": {"site": SiteSitemap}},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("", include("core.urls")),
    path("admin/", admin.site.urls),
    path("tinymce/", include("tinymce.urls")),
    # catch any other urls and check
    # if they are static page urls
    re_path(r"^(?P<url_path>.*)/$", static_page, name="static_page"),
]
