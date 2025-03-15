import os

from django.conf import settings
from django.shortcuts import render


def main_page(request):
    return render(request, "index.html")


def readme_view(request):
    readme_path = os.path.join(settings.BASE_DIR, "..", "README.md")

    with open(readme_path, "r", encoding="utf-8") as readme_file:
        readme_content = readme_file.read()

    return render(request, "readme.html", {"readme_content": readme_content})
