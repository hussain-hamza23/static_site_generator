import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node
from htmlnode import ParentNode


def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No title found in markdown")


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(
        f"Generating page from {from_path} using template {template_path} to {dest_path}"
    )

    with open(from_path, "r") as markdown:
        markdown_content: str = markdown.read()
    with open(template_path, "r") as template:
        template_content: str = template.read()

    html_node: ParentNode = markdown_to_html_node(markdown_content)
    title: str = extract_title(markdown_content)
    html_string: str = html_node.to_html()
    template_content = template_content.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_string
    )

    try:
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    except OSError as e:
        print(f"Error creating directories for {dest_path}: {e}")

    with open(dest_path, "w") as output:
        output.write(template_content)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
):
    for entry in os.listdir(dir_path_content):
        path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)
        if os.path.isfile(path):
            dest_path: str = str(Path(dest_path).with_suffix(".html"))
            generate_page(path, template_path, dest_path)
        else:
            generate_pages_recursive(path, template_path, dest_path)
