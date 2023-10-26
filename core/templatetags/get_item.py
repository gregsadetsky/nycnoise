from django.template.defaulttags import register


@register.filter
def get_item(dicti, key):
    return dicti[key]
