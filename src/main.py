import os
import shutil
import sys
from constants import (
    CONTENT_PATH,
    PUBLIC_DIR,
    STATIC_DIR,
    CONTENT_FILE,
    TEMPLATE_FILE,
    OUTPUT_FILE,
    DOCS_PATH,
)
from generate_page.copy import copy_contents
from generate_page.extraction import generate_pages_recursive


def main():
    basepath: str = sys.argv[1] if len(sys.argv) > 1 else "/"

    print("Deleting public directory....")
    if os.path.exists(PUBLIC_DIR):
        shutil.rmtree(PUBLIC_DIR)

    print(f"Copying contents in {STATIC_DIR} to {PUBLIC_DIR}")
    copy_contents(STATIC_DIR, PUBLIC_DIR)

    print(
        f"Generating page from {CONTENT_FILE} using template {TEMPLATE_FILE} to {OUTPUT_FILE}"
    )
    # generate_page(CONTENT_FILE, TEMPLATE_FILE, OUTPUT_FILE)
    generate_pages_recursive(basepath, CONTENT_PATH, TEMPLATE_FILE, DOCS_PATH)


if __name__ == "__main__":
    main()
