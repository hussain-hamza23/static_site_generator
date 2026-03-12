from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode
import re


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    split_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            split_nodes.append(node)
            continue
        text: list[str] = node.text.split(delimiter)
        if len(text) % 2 == 0:
            raise ValueError(f"Invalid markdown format in text: {node.text}")
        for i, part in enumerate(text):
            if part:
                split_nodes.append(
                    TextNode(part, TextType.TEXT if i % 2 == 0 else text_type),
                )
    return split_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_images(old_nodes: list[TextNode]) -> list[TextNode]:
    split_nodes: list[TextNode] = []
    for node in old_nodes:
        images: list[tuple[str, str]] = extract_markdown_images(node.text)

        if node.text_type != TextType.TEXT or not images:
            split_nodes.append(node)
            continue

        if len(images) == 0:
            split_nodes.append(node)
            continue

        def split_text(
            text: str, images: list[tuple[str, str]], memo: list[str | tuple[str, str]]
        ) -> list[str | tuple[str, str]]:
            if not images:
                if text:
                    memo.append(text)
                return memo
            image_alt, image_url = images[0]
            section = text.split(f"![{image_alt}]({image_url})", 1)

            if len(section) != 2:
                raise ValueError(f"Invalid markdown: image not found")
            if section[0]:
                memo.append(section[0])
            memo.append(images[0])
            return split_text(section[1], images[1:], memo)

        sections = split_text(node.text, images, [])
        for section in sections:
            if isinstance(section, str):
                split_nodes.append(TextNode(section, TextType.TEXT))
            elif isinstance(section, tuple):
                split_nodes.append(TextNode(section[0], TextType.IMAGE, section[1]))

    return split_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    split_nodes: list[TextNode] = []
    for node in old_nodes:
        links: list[tuple[str, str]] = extract_markdown_links(node.text)
        if node.text_type != TextType.TEXT or not links:
            split_nodes.append(node)
            continue

        if len(links) == 0:
            split_nodes.append(node)
            continue

        def split_text(
            text: str, links: list[tuple[str, str]], memo: list[str | tuple[str, str]]
        ) -> list[str | tuple[str, str]]:
            if not links:
                if text:
                    memo.append(text)
                return memo
            link_text, link_url = links[0]
            section = text.split(f"[{link_text}]({link_url})", 1)

            if len(section) != 2:
                raise ValueError(f"Invalid markdown: link not found")
            if section[0]:
                memo.append(section[0])
            memo.append(links[0])
            return split_text(section[1], links[1:], memo)

        sections = split_text(node.text, links, [])

        for section in sections:
            if isinstance(section, str):
                split_nodes.append(TextNode(section, TextType.TEXT))
            elif isinstance(section, tuple):
                split_nodes.append(TextNode(section[0], TextType.LINK, section[1]))

    return split_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    old_nodes: list[TextNode] = [TextNode(text, TextType.TEXT)]
    split_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
    split_nodes = split_nodes_delimiter(split_nodes, "_", TextType.ITALIC)
    split_nodes = split_nodes_delimiter(split_nodes, "`", TextType.CODE)
    split_nodes = split_nodes_images(split_nodes)
    split_nodes = split_nodes_link(split_nodes)

    return split_nodes


def text_to_children(text: str) -> list[HTMLNode]:
    inline_nodes: list[TextNode] = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in inline_nodes]
