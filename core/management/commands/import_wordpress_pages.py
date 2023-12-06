import re
from argparse import RawTextHelpFormatter

import lxml.etree as etree
from bs4 import BeautifulSoup
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
        parser.add_argument(
            "--delete_all_pages_absolutely_for_sure", default=False, action="store_true"
        )

    def handle(self, *args, **options):
        if options["delete_all_pages"]:
            user_response = input(
                "About to delete all pages. Are you absolutely sure? Type yes > "
            )
            if user_response != "yes":
                raise CommandError("Aborting")
            StaticPage.objects.all().delete()
        if options["delete_all_pages_absolutely_for_sure"]:
            StaticPage.objects.all().delete()

        file_to_wordpress_export_xml_file = options["file_to_wordpress_export_xml_file"]

        parser = etree.XMLParser(strip_cdata=False)
        with open(file_to_wordpress_export_xml_file, encoding="UTF-8") as f:
            content = f.read()

            # manually clean up gremlins
            content = content.replace(chr(3), "")
            content = content.replace(chr(8), "")
            content = content.replace(chr(0x1F), "")
            content = content.replace(chr(0xA0), " ")

            soup = etree.fromstring(content.encode("utf-8"), parser=parser)
            # absolutely necessary to have this 'prefix map', otherwise
            # the xml parser won't be able to find tags. why.
            prefix_map = {
                "wp": "http://wordpress.org/export/1.2/",
                "content": "http://purl.org/rss/1.0/modules/content/",
            }

            imported_pages = 0
            # find all <item> sub-children by xpath
            for item in soup.xpath("//item"):
                if item.find("wp:post_type", prefix_map).text not in ["page", "post"]:
                    continue

                url_path = item.find("link").text.replace("https://nyc-noise.com/", "")
                if url_path == "":
                    # skip the homepage
                    continue
                # strip slash
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

                # table of contents, bringing in bs4 because lxml (ligmaXML) is annoying
                bs = BeautifulSoup(content, "html.parser")
                table = "<table class='toc'><th>Table of Contents</th>"

                # iterate over all h1, h2 and h3 headers
                for header in bs.find_all(["h1", "h2", "h3"]):
                    # standardize header.text by making it safe (remove any weird chars)
                    # to create an inner-page tag
                    href = re.sub(r"[\W]+", "_", header.text.lower()).strip("_")
                    # Need to apply this to the content
                    header["id"] = href
                    # Building the table
                    row = "<span>" + header.text + "</span>"
                    # add a class to the <a> of link-h1 for h1, etc.
                    row = f"<tr><td><a class='link-{header.name}' href='#{href}'>{row}</a></td></tr>"
                    table += row

                # Apply the changes
                content = str(bs)
                # Close the table
                table += "</table>"
                # Replace the wordpress widget block with our table of contents
                pattern = re.compile(r"(\[lwptoc.*?\])")
                content = pattern.sub(table, content)

                # match bandcamp embeds, and replace them with embeds
                # [bandcamp width=100% height=120 track=545233516 size=large bgcol=ffffff linkcol=0687f5 tracklist=false artwork=small]
                # should become
                # <iframe width="100%" height="120" style="position: relative; display: block; width: 100%; height: 120px;" src="//bandcamp.com/EmbeddedPlayer/v=2/track=545233516/size=large/bgcol=ffffff/linkcol=0687f5/tracklist=false/artwork=small/" allowtransparency="true" frameborder="0"></iframe>
                # it can also be album=.... and it should then have /v=2/album=...
                content = re.sub(
                    r"\[bandcamp width=([^\s]+) height=([^\s]+) (track|album)=([^\s]+) size=([^\s]+) bgcol=([^\s]+) linkcol=([^\s]+) tracklist=([^\s]+) artwork=(\w+)\]",
                    r'<iframe width="\1" height="\2" style="position: relative; display: block; width: \1; height: \2;" src="//bandcamp.com/EmbeddedPlayer/v=2/\3=\4/size=\5/bgcol=\6/linkcol=\7/tracklist=\8/artwork=\9/" allowtransparency="true" frameborder="0"></iframe>',
                    content,
                )

                # match youtube embeds which are JUST youtube hyperlinks on new lines....!!!
                youtube_replacement_str = r'<iframe width="560" height="315" src="https://www.youtube.com/embed/\1" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>'
                content = re.sub(
                    r"<p>https://www.youtube.com/watch\?v=(.{11})</p>",
                    youtube_replacement_str,
                    content,
                )
                # same for different youtube format
                content = re.sub(
                    r"<p>https://youtu.be/(.{11})</p>", youtube_replacement_str, content
                )

                # hack <img>s to point to the s3 bucket
                content = re.sub(
                    # this is the "11.3-flyer-lineup-1024x1024.png" format where the "-1024x1024" part
                    # is dynamically added/handled by wp to do on the fly image resizing. we only match the real filename
                    r'<img([^>]+)src="https://nyc-noise.com/wp-content/uploads/([^"]+)-\d+x\d+\.(\w+)(\?crop=1|)"([^>]*)>',
                    r'<img\1src="https://nyc-noise-wp-files.s3.us-east-2.amazonaws.com/wp-content/uploads/\2.\3"\5>',
                    content,
                )
                # simpler remaining case of <img>s that link directly to real files
                content = re.sub(
                    r'<img([^>]+)src="https://nyc-noise.com/wp-content/uploads/([^"\?]+)(\?crop=1|)"([^>]*)>',
                    r'<img\1src="https://nyc-noise-wp-files.s3.us-east-2.amazonaws.com/wp-content/uploads/\2"\4>',
                    content,
                )

                # make weird inert <a href="https://nyc-noise.com/?attachment_id=40606"> link inert by linking to #
                content = re.sub(
                    r'<a href="https://nyc-noise.com/\?attachment_id=\d+">',
                    r'<a href="#">',
                    content,
                )

                StaticPage.objects.create(
                    url_path=url_path, title=title, content=content
                )
                imported_pages += 1

        self.stdout.write(self.style.SUCCESS(f"Imported {imported_pages} pages"))
