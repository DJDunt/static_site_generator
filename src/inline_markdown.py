
from textnode import TextType,TextNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise Exception(f"Thats invlid markdown, delimiter {delimiter} is not closed")
        for i, text in enumerate(split_text):
            if text == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(text, TextType.TEXT))
            else:
                new_nodes.append(TextNode(text, text_type))
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        split_text = re.split(r"!\[[^\[\]]*\]\([^\(\)]*\)", node.text)
        for i, text in enumerate(split_text):
            if text:
                new_nodes.append(TextNode(text, TextType.TEXT))
            if i < len(images):
                alt_text, url = images[i]
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        split_text = re.split(r"(?<!!)\[[^\[\]]*\]\([^\(\)]*\)", node.text)
        for i, text in enumerate(split_text):
            if text:
                new_nodes.append(TextNode(text, TextType.TEXT))
            if i < len(links):
                link_text, url = links[i]
                new_nodes.append(TextNode(link_text, TextType.LINK, url))
    return new_nodes

def text_to_textnodes(text):
    initial_list = [TextNode(text, TextType.TEXT)]
    list_bold = split_nodes_delimiter(initial_list, "**", TextType.BOLD)
    list_italic = split_nodes_delimiter(list_bold, "_", TextType.ITALIC)
    list_code = split_nodes_delimiter(list_italic, "`", TextType.CODE)
    list_images = split_nodes_image(list_code)
    list_links = split_nodes_link(list_images)
    text_node_objects = list_links
    return text_node_objects
    