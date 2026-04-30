from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_markdown import markdown_to_blocks, text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith(("###### ", "##### ", "#### ", "### ", "## ", "# ")):
        return BlockType.HEADING
    elif lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    elif block.startswith((">", "> ")):
        i = 1
        for line in lines:
            if not line.startswith(("> ", ">")):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif block.startswith(("- ")):
        i = 1
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif block.startswith(("1. ")):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            children.append(paragraph_to_html_node(block))
        elif block_type == BlockType.HEADING:
            children.append(headings_to_html_node(block))
        elif block_type == BlockType.CODE:
            children.append(code_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            children.append(quote_to_html_node(block))
        elif block_type == BlockType.UNORDERED_LIST:
            children.append(ulist_to_html_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            children.append(olist_to_html_node(block))
    return ParentNode("div", children)

def text_to_children(text):
    transformers = text_to_textnodes(text)
    transformed_list = []
    for transformer in transformers:
        transformed = text_node_to_html_node(transformer)
        transformed_list.append(transformed)
    return transformed_list

def headings_to_html_node(block):
    depth = 0
    for char in block:
        if char == "#":
            depth += 1
            if depth > 6:
                raise Exception("nah fam, this is too many #'s")
        else:
            break
    content = block[depth:].strip()
    if block[depth] != " ":
        raise ValueError("must start with space")
    return ParentNode(f"h{depth}", text_to_children(content))


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    parachild = text_to_children(paragraph)
    return ParentNode("p", parachild)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise Exception("that's no code")
    inner = block[4:-3]
    text_node = TextNode(inner, TextType.TEXT)
    html_node = text_node_to_html_node(text_node)
    code_node = ParentNode("code", [html_node])
    return ParentNode("pre", [code_node])

def quote_to_html_node(block):
    lines = block.split("\n")
    cleaned = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote line")
        cleaned.append(line.lstrip(">").strip())
    text = " ".join(cleaned)
    return ParentNode("blockquote", text_to_children(text))

def ulist_to_html_node(block):
    lines = block.split("\n")
    items = []
    for line in lines:
        text = line[2:]
        children = text_to_children(text)
        items.append(ParentNode("li", children))
    return ParentNode("ul", items)

def olist_to_html_node(block):
    lines = block.split("\n")
    items = []
    for i, line in enumerate(lines):
        prefix_len = len(str(i + 1)) + 2
        text = line[prefix_len:]
        children = text_to_children(text)
        items.append(ParentNode("li", children))
    return ParentNode("ol", items)