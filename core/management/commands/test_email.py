from core.utils_aws import aws_mail_sender
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        aws_mail_sender.send_email(
            "hi@greg.technology",
            "contact+submissions@nyc-noise.com",
            "this is the subject",
            "this is the content",
            "and this is the html version",
        )
