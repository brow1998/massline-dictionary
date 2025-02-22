import os
import re
import unicodedata

from markdownify import markdownify as md
from scrapy import Request
from scrapy.pipelines.files import FilesPipeline
from scrapy.utils.project import get_project_settings


def slugify(value, max_length=50):
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value)
    value = value.strip().lower()
    slug = re.sub(r"[-\s]+", "_", value)

    if slug.startswith("lgbt"):
        slug = "lgbt"

    return slug[:max_length]


def replace_link(match):
    text = match.group(1).replace("\n", " ").strip()
    url = match.group(2).replace("\n", "").strip()
    new_url = url
    if url.startswith("#"):
        new_url = url[1:].lower() + ".md"
    elif "#" in url:
        fragment = url.split("#")[-1]
        new_url = fragment.lower() + ".md"
    elif url.lower().endswith(".htm"):
        base = os.path.splitext(os.path.basename(url))[0].lower()
        new_url = slugify(base) + ".md"
    return f"[{text}]({new_url})"


def replace_image_link(match):
    settings = get_project_settings()
    images_path = settings.get('FILES_STORE', 'images')

    alt_text = match.group(1)
    url = match.group(2).strip()
    file_name = os.path.basename(url)

    relative_path = os.path.relpath(images_path, start=os.getcwd())

    new_url = f"{relative_path}/{file_name}"
    return f"![{alt_text}]({new_url})"


class MarkdownFilePipeline:
    def __init__(self, settings):
        settings = get_project_settings()
        self.items_output_path = settings.get('ITEMS_OUTPUT_PATH', 'output')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_item(self, item, spider):
        markdown_content = md(item["body"])

        markdown_content = re.sub(
            r"\[([^\]]+)\]\(([^)]+)\)", replace_link, markdown_content, flags=re.DOTALL
        )

        markdown_content = re.sub(
            r"!\[([^\]]*)\]\(([^)]+)\)",
            replace_image_link,
            markdown_content,
            flags=re.DOTALL,
        )

        os.makedirs(self.items_output_path, exist_ok=True)

        file_name = slugify(item["title"]) + ".md"
        file_path = os.path.join(self.items_output_path, file_name)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        spider.logger.info(f"Saving file at: {file_path}")
        return item


class CustomImagePipeline(FilesPipeline):
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = super().from_crawler(crawler)  # Chama a inicialização da FilesPipeline corretamente
        files_store = crawler.settings.get("FILES_STORE", "images")
        pipeline.images_output_path = os.path.abspath(files_store)

        return pipeline

    def get_media_requests(self, item, info):
        if "image_urls" in item and item["image_urls"]:
            for image_url in item["image_urls"]:
                info.spider.logger.info(f"Downloading image: {image_url}")
                yield Request(image_url)

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = os.path.basename(request.url)
        return image_guid