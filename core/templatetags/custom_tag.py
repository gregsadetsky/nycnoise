from django.template.Library import register


@register.filter
def keyvalue(dicti, key):
    return dicti[key]
