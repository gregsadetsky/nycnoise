from core.models import MenuItem
from django.template.defaulttags import register


@register.simple_tag
def get_header_menu_items():
    return MenuItem.objects.filter(show_in_header=True)


@register.simple_tag
def get_all_menu_items():
    return MenuItem.objects.all()


@register.simple_tag
def get_footer_menu_items():
    return MenuItem.objects.filter(show_in_footer=True)
