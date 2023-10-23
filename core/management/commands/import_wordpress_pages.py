from argparse import RawTextHelpFormatter

import lxml.etree as etree
from core.models import StaticPage
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = """
        Imports "static" pages from a nyc-noise.com wordpress xml dump.
        The goal is to recreate all existing pages from nyc-noise.com pages, for example:
        - https://nyc-noise.com/bandcamp-roundup/
        - https://nyc-noise.com/about/
        etc.
        Ideally, we'd want all of the existing urls (e.g., /about/) to be perfectly
        ported over to the new site. Which means the page's <title>, the opengraph tags,
        the url, the rich text content and the images should all port over seemlessly.
        TODO a lot of these things are not handled by the code below :-)
    """.strip()

    # customization so that above help string keeps its newlines when printed to the console
    # https://stackoverflow.com/a/35470682
    def create_parser(self, *args, **kwargs):
        parser = super(Command, self).create_parser(*args, **kwargs)
        parser.formatter_class = RawTextHelpFormatter
        return parser

    def add_arguments(self, parser):
        parser.add_argument("file_to_wordpress_export_xml_file")
        parser.add_argument("--delete_all_pages", default=False, action="store_true")

    def handle(self, *args, **options):
        if options["delete_all_pages"]:
            user_response = input(
                "About to delete all pages. Are you absolutely sure? Type yes > "
            )
            if user_response != "yes":
                raise CommandError("Aborting")
            StaticPage.objects.all().delete()

        file_to_wordpress_export_xml_file = options["file_to_wordpress_export_xml_file"]

        parser = etree.XMLParser(strip_cdata=False)
        with open(file_to_wordpress_export_xml_file) as f:
            content = f.read()

            # manually clean up gremlins
            content = content.replace(chr(3), "")
            content = content.replace(chr(8), "")
            content = content.replace(chr(0x1F), "")
            content = content.replace(chr(0xA0), " ")

            soup = etree.fromstring(content.encode("utf-8"), parser=parser)
            prefix_map = {
                "wp": "http://wordpress.org/export/1.2/",
                "content": "http://purl.org/rss/1.0/modules/content/",
            }

            imported_pages = 0
            # find all <item> sub-children by xpath
            for item in soup.xpath("//item"):
                if item.find("wp:post_type", prefix_map).text != "page":
                    continue

                url_path = item.find("link").text.replace("https://nyc-noise.com/", "")
                # strip slash
                if url_path == "":
                    # skip the homepage
                    continue
                if url_path[-1] == "/":
                    url_path = url_path[:-1]

                title = item.find("title").text

                content = item.find("content:encoded", prefix_map).text
                # wordpress half encodes content in html and uses \n\n as an indicator
                # of stuff to encode with <p>... un-do that.
                content = "".join(
                    [f"<p>{paragraph}</p>" for paragraph in content.split("\n\n")]
                )
                content = content.replace("\n", "<br/>")
                # not great. but works.
                content = content.replace("</h2><br/>", "</h2>")

                StaticPage.objects.create(
                    url_path=url_path, title=title, content=content
                )
                imported_pages += 1

        self.stdout.write(self.style.SUCCESS(f"Imported {imported_pages} pages"))
