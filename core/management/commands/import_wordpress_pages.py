from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("file_to_wordpress_export_xml_file")

    def handle(self, *args, **options):
        file_to_wordpress_export_xml_file = options["file_to_wordpress_export_xml_file"]
        self.stdout.write(
            self.style.SUCCESS(
                f"Importing pages from {file_to_wordpress_export_xml_file}"
            )
        )
        from core.models import Page

        Page.objects.all().delete()
        from core.utils import import_wordpress_pages

        import_wordpress_pages(file_to_wordpress_export_xml_file)
        self.stdout.write(self.style.SUCCESS("Done!"))
