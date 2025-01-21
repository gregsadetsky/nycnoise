import uuid

from core.models import StaticPage


def create_static_test_page():
    page_path = str(uuid.uuid4())
    page_title = str(uuid.uuid4())
    page_content = str(uuid.uuid4())
    return StaticPage.objects.create(
        url_path=page_path, title=page_title, content=page_content
    )
