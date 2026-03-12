import os
import shutil
import sys
from constants import (
    CONTENT_PATH,
    STATIC_DIR,
    TEMPLATE_FILE,
    DOCS_PATH,
)
from generate_page.copy import copy_contents
from generate_page.extraction import generate_pages_recursive


def main():
    basepath: str = sys.argv[1] if len(sys.argv) > 1 else "/"

    print("Deleting docs directory....")
    if os.path.exists(DOCS_PATH):
        shutil.rmtree(DOCS_PATH)

    print(f"Copying contents in {STATIC_DIR} to {DOCS_PATH}")
    copy_contents(STATIC_DIR, DOCS_PATH)

    print(
        f"Generating page from {CONTENT_PATH} using template {TEMPLATE_FILE} to {DOCS_PATH}"
    )
    generate_pages_recursive(basepath, CONTENT_PATH, TEMPLATE_FILE, DOCS_PATH)


if __name__ == "__main__":
    main()
