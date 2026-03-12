import os
import shutil
from constants import (
    CONTENT_PATH,
    PUBLIC_DIR,
    STATIC_DIR,
    CONTENT_FILE,
    TEMPLATE_FILE,
    OUTPUT_FILE,
    OUTPUT_PATH,
)
from generate_page.copy import copy_contents
from generate_page.extraction import generate_pages_recursive


def main():
    print("Deleting public directory....")
    if os.path.exists(PUBLIC_DIR):
        shutil.rmtree(PUBLIC_DIR)

    print(f"Copying contents in {STATIC_DIR} to {PUBLIC_DIR}")
    copy_contents(STATIC_DIR, PUBLIC_DIR)

    print(
        f"Generating page from {CONTENT_FILE} using template {TEMPLATE_FILE} to {OUTPUT_FILE}"
    )
    # generate_page(CONTENT_FILE, TEMPLATE_FILE, OUTPUT_FILE)
    generate_pages_recursive(CONTENT_PATH, TEMPLATE_FILE, OUTPUT_PATH)


if __name__ == "__main__":
    main()
