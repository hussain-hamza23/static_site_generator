import os


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC_DIR = os.path.join(ROOT_DIR, "public")
STATIC_DIR = os.path.join(ROOT_DIR, "static")

CONTENT_PATH = os.path.join(ROOT_DIR, "content")
OUTPUT_PATH = os.path.join(ROOT_DIR, "public")

CONTENT_FILE = os.path.join(CONTENT_PATH, "index.md")
TEMPLATE_FILE = os.path.join(ROOT_DIR, "template.html")
OUTPUT_FILE = os.path.join(PUBLIC_DIR, "index.html")
