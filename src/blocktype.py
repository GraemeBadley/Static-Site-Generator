from enum import Enum
from htmlnode import *
from delimiter import text_to_textnodes
from textnode import text_node_to_html_node
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(md):

    lines = md.split("\n")

    if md.startswith(("#","##","###","####","#####","######")):
        return BlockType.HEADING
    if md.startswith("```") and md.endswith("```"):
        return BlockType.CODE
    if md.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if md.startswith("-"):
        for line in lines:
            if not line.startswith("-"):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if md.startswith("1. "):
        line_num = 0
        for line in lines:
            line_num += 1
            if not line.startswith(f"{line_num}. "):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks if block]

    return blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    body = []
    for block in blocks:
        type = block_to_block_type(block)
        if type == BlockType.PARAGRAPH:
            block = block.replace("\n"," ")
            node = ParentNode("p",children=[])
            node.children = text_to_children(block)
            body.append(node)
        if type == BlockType.QUOTE:
            block = block.replace("\n"," ")
            block = block.replace("> ", "")
            node = ParentNode("blockquote",children=[])
            node.children = text_to_children(block)
            body.append(node)
        if type == BlockType.HEADING:
            block = block.replace("\n"," ")
            heading_num = block.count('#',0,block.find(" "))
            node = ParentNode(f"h{heading_num}",children=[])
            node.children = text_to_children(block[block.find(" ")+1:])
            body.append(node)
        if type == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            lines = [x.replace("- ","") for x in lines]
            list_node = ParentNode('ul',children=[])
            for line in lines:
                node = ParentNode(f"li",children=[])
                node.children = text_to_children(line)
                list_node.children.append(node)
            body.append(list_node)
        if type == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            lines = [re.sub(r'^\d+\. ',"",x) for x in lines]
            list_node = ParentNode('ol',children=[])
            for line in lines:
                node = ParentNode("li",children=[])
                node.children = text_to_children(line)
                list_node.children.append(node)
            body.append(list_node)
        if type == BlockType.CODE:
            node_pre = ParentNode("pre",children=[])
            node_code = ParentNode("code",children=[])
            new_text = block.replace("```","").replace('\n','',1)
            node = LeafNode("",new_text)
            node_code.children.append(node)
            node_pre.children.append(node_code)
            body.append(node_pre)

    return ParentNode("div",body)

def text_to_children(text):
    nodes = text_to_textnodes(text)
    html_nodes = []
    for node in nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes
        
def main():
    md = md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
    print(markdown_to_html_node(md).to_html())

main()

