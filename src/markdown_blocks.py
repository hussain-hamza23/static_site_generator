from enum import Enum
from htmlnode import ParentNode
from inline import text_to_children
from textnode import TextNode, TextType, text_node_to_html_node


def markdown_to_blocks(markdown: str) -> list[str]:
    lines = markdown.split("\n\n")
    return [stripped for line in lines if (stripped := line.strip())]


BlockType = Enum(
    "BlockType",
    ["PARAGRAPH", "HEADING", "CODE", "QUOTE", "UNORDERED_LIST", "ORDERED_LIST"],
)


def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")

    match block:
        case b if b.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
            return BlockType.HEADING
        case b if b.startswith("```") and b.endswith("```") and len(lines) > 1:
            return BlockType.CODE
        case b if all(line.startswith(">") for line in lines):
            return BlockType.QUOTE
        case b if all(line.startswith("- ") for line in lines):
            return BlockType.UNORDERED_LIST
        case b if b.startswith("1. "):
            for i, line in enumerate(lines, start=1):
                if not line.startswith(f"{i}. "):
                    return BlockType.PARAGRAPH
            return BlockType.ORDERED_LIST
        case _:
            return BlockType.PARAGRAPH


def clean_block(block: str) -> list[str]:
    lines = block.split("\n")
    return [line.strip() for line in lines if line.strip()]


def list_to_html_node(block: str, block_type: BlockType) -> ParentNode:
    clean_lines: list[str] = clean_block(block)
    if block_type == BlockType.UNORDERED_LIST:
        tag, cleaned_lines = "ul", [line[2:] for line in clean_lines]
    elif block_type == BlockType.ORDERED_LIST:
        tag, cleaned_lines = "ol", []
        for i, line in enumerate(clean_lines, start=1):
            cleaned_lines.append(line[len(f"{i}. ") :])
    else:
        raise ValueError(f"Block type {block_type} is not a list")

    li_nodes: list[ParentNode] = []
    for line in cleaned_lines:
        li_node = ParentNode("li", text_to_children(line))
        li_nodes.append(li_node)

    return ParentNode(tag, li_nodes)


def code_to_html_node(block: str) -> ParentNode:
    code_format = block[4:-3]
    code_node: TextNode = TextNode(code_format, TextType.TEXT)
    code_inner: ParentNode = ParentNode("code", [text_node_to_html_node(code_node)])
    return ParentNode("pre", [code_inner])


def heading_to_html_node(block: str) -> ParentNode:
    level = block.count("#", 0, 6)
    heading_block = "\n".join(line[level + 1 :] for line in clean_block(block))
    return ParentNode(f"h{level}", text_to_children(heading_block))


def quote_to_html_node(block: str) -> ParentNode:
    cleaned_quote = " ".join(line[2:] for line in clean_block(block))
    return ParentNode("blockquote", text_to_children(cleaned_quote))


def paragraph_to_html_node(block: str) -> ParentNode:
    cleaned_paragraph = " ".join(clean_block(block))
    return ParentNode("p", text_to_children(cleaned_paragraph))


def block_to_node(block: str, block_type: BlockType) -> ParentNode:
    match block_type:
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.UNORDERED_LIST | BlockType.ORDERED_LIST:
            return list_to_html_node(block, block_type)
        case _:
            raise ValueError(f"Unsupported block type: {block_type}")


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks: list[str] = markdown_to_blocks(markdown)
    html_nodes: list[ParentNode] = []

    for block in blocks:
        block_type: BlockType = block_to_block_type(block)
        block_node: ParentNode = block_to_node(block, block_type)
        html_nodes.append(block_node)
    return ParentNode("div", html_nodes)
