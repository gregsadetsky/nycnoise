from django.contrib.admin.templatetags.admin_modify import register
from django.contrib.admin.templatetags.admin_modify import (
    submit_row as original_submit_row,
)


@register.inclusion_tag("admin/submit_line.html", takes_context=True)
def submit_row(context):
    """
    Overrides 'django.contrib.admin.templatetags.admin_modify.submit_row'.

    https://stackoverflow.com/questions/13101281
    and
    https://github.com/openedx/django-config-models/blob/master/config_models/templatetags.py
    """

    ctx = original_submit_row(context)
    if context.get("show_save", True):
        ctx.update(
            {
                # show all the save buttons!
                # this is not normally possible using 'regular' django admin options
                "show_save_as_new": True,
                "show_save_and_add_another": True,
                "show_save_and_continue": True,
            }
        )

    return ctx
