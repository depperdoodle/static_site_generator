from textnode import TextType, TextNode
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes_list.append(old_node)
        else:
            pieces = old_node.text.split(delimiter)
            if len(pieces) % 2 == 0:
                raise Exception(f"no matches found")
            
            else:
                for i, piece in enumerate(pieces):
                    if i % 2 == 0:
                        if piece:
                            new_nodes_list.append(TextNode(piece, TextType.TEXT))
                    else:
                        new_nodes_list.append(TextNode(piece, text_type))
    return new_nodes_list


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes_list.append(old_node)
        else:
            matches = extract_markdown_images(old_node.text)
            if not matches:
                new_nodes_list.append(old_node)
                continue
            remaining_text = old_node.text
            for alt, url in matches:
                sections = remaining_text.split(f"![{alt}]({url})", 1)
                if sections[0]:
                    new_nodes_list.append(TextNode(sections[0], TextType.TEXT))
                new_nodes_list.append(TextNode(alt, TextType.IMAGE, url))
                remaining_text = sections[1]
            if remaining_text:
                new_nodes_list.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes_list
            
def split_nodes_link(old_nodes):
    new_nodes_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes_list.append(old_node)
        else:
            matches = extract_markdown_links(old_node.text)
            if not matches:
                new_nodes_list.append(old_node)
                continue
            remaining_text = old_node.text
            for alt, url in matches:
                sections = remaining_text.split(f"[{alt}]({url})", 1)
                if sections[0]:
                    new_nodes_list.append(TextNode(sections[0], TextType.TEXT))
                new_nodes_list.append(TextNode(alt, TextType.LINK, url))
                remaining_text = sections[1]
            if remaining_text:
                new_nodes_list.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes_list


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    stripped_split = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        stripped = block.strip()
        if stripped == "":
            continue
        stripped_split.append(stripped)
    return stripped_split