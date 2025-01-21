from meta.views import Meta
from django.templatetags.static import static


def get_meta(
    url=None,
    title="nyc noise",
    description=(
        "NYC experimental live music calendar • noise, improv, jazz, new music,"
        " avant-electronics, weirdos • performance against corporate interests!"
    ),
):
    return Meta(
        title=title,
        url=f"{url or ''}/",
        description=description,
        image=static("core/images/NYC-Noise-facebook-preview-TOO-BIG.png"),
    )
