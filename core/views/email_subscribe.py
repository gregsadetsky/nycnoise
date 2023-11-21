from django.shortcuts import redirect, render

from ..models import EmailSubscriber


def email_subscribe(request):
    if request.method == "GET":
        return render(request, "core/email_subscribe_thanks.html")

    assert request.method == "POST"

    email_address = request.POST["email"]
    # don't try to re-create if someone re-subscribes.
    # 'email' field is marked as unique in model, which
    # would create an error if we did attempt to re-create object
    # for same email address
    EmailSubscriber.objects.get_or_create(email=email_address)

    # redirect from POST to GET to avoid 'do you want to submit...'
    # on clicking back
    return redirect("email_subscribe")
