from django import template

register = template.Library()


@register.simple_tag
def meta_title():
    return "NYC Noise"


@register.simple_tag
def meta_description():
    return "NYC experimental live music calendar • noise, improv, jazz, new music, avant-electronics, weirdos • performance against corporate interests!"


@register.simple_tag
def meta_domain():
    return "nyc-noise.com"


@register.simple_tag
def meta_url(url="/"):
    return f"https://{meta_domain()}{url}"