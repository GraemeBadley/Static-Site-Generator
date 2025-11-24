from textnode import TextType,TextNode

import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception(f"Invalid syntax, Missing closing {delimiter}, ")
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 ==0:
                new_nodes.append(TextNode(parts[i],TextType.TEXT))
            else:
                new_nodes.append(TextNode(parts[i],text_type))

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
        imgs = extract_markdown_images(node.text)
        if not imgs:
            new_nodes.append(node)
            continue
        
        text = node.text

        parts = re.split(r"(!\[[^\[\]]*\]\([^\(\)]*\))",text )
            
            
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 ==0:
                new_nodes.append(TextNode(parts[i],TextType.TEXT))
            else:
                new_nodes.append(TextNode(imgs[int((i-1)/2)][0],TextType.IMAGE,imgs[int((i-1)/2)][1]))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        imgs = extract_markdown_links(node.text)
        if not imgs:
            new_nodes.append(node)
            continue
        
        text = node.text

        parts = re.split(r"(?<!!)(\[[^\[\]]*\]\([^\(\)]*\))",text )
            
            
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 ==0:
                new_nodes.append(TextNode(parts[i],TextType.TEXT))
            else:
                new_nodes.append(TextNode(imgs[int((i-1)/2)][0],TextType.LINK,imgs[int((i-1)/2)][1]))

    return new_nodes  

def text_to_textnodes(text):
    node = TextNode(text,TextType.TEXT)
    bold = split_nodes_delimiter([node],"**",TextType.BOLD)
    italic = split_nodes_delimiter(bold,"_",TextType.ITALIC)
    code = split_nodes_delimiter(italic,"`",TextType.CODE)
    return split_nodes_link(split_nodes_image(code))

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks if block]

    return blocks


def main():
    md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
    blocks = markdown_to_blocks(md)
    print(blocks)

if __name__ == "__main__":
    main()