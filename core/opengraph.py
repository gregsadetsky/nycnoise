from meta.views import Meta
from django.templatetags.static import static


def get_meta(url='/'):
    return Meta(
        title="nyc noise",
        url=url,
        object_type='website',
        description=(
            "NYC experimental live music calendar • noise, improv, jazz, new music,"
            " avant-electronics, weirdos • performance against corporate interests!"
        ),
        twitter_type="summary_large_image",
        image=static("images/NYC-Noise-facebook-preview-TOO-BIG.png"),
    )
