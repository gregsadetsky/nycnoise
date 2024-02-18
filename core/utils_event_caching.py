from django.template.loader import get_template


def bake_event_html(event):
    template = get_template("core/event.html")
    return template.render(
        {
            "event": event,
        }
    )
