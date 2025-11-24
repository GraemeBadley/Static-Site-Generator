import shutil
from textnode import TextNode
import os
from blocktype import markdown_to_html_node

def main():
    copy_dir("/home/gbadley/boot-dev-course/Static-Site-Generator/static","/home/gbadley/boot-dev-course/Static-Site-Generator/public")
    #generate_page("content/index.md","template.html","public/index.html")
    generate_pages_recursive("content","template.html","public")

def copy_dir(source,destination):
    shutil.rmtree(destination)
    os.mkdir(destination)
    files = os.listdir(source)
    for file in files:
        file_path = os.path.join(source,file)
        if os.path.isfile(file_path):
            shutil.copy(file_path,destination)
        else:
            new_dir = os.path.join(destination,file)
            os.mkdir(new_dir)
            copy_dir(file_path,new_dir)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        line = line.strip()
        if line.startswith("# "):
            return line.replace("# ","")
        
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    items = os.listdir(dir_path_content)
    for item in items:
        file_path = os.path.join(dir_path_content,item)
        if os.path.isfile(file_path):
            print(f'{item} is a file')
            item = item.replace(".md",".html")
            dest_path = os.path.join(dest_dir_path,item)
            generate_page(file_path,template_path,dest_path)
        else:
            print(f'{item} is a dir')
            new_dir = os.path.join(dir_path_content,item)
            new_dest_dir = os.path.join(dest_dir_path,item)
            os.mkdir(new_dest_dir)
            generate_pages_recursive(new_dir,template_path,new_dest_dir)
    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(file=from_path,mode='r',encoding='utf-8') as reader:
        content = reader.read()
        reader.close()

    with open(file=template_path,mode='r',encoding='utf-8') as reader:
        template = reader.read()
        reader.close()
    
    html_node = markdown_to_html_node(content)

    html = html_node.to_html()
    title = extract_title(content)
    new_html = template.replace("{{ Title }}",title).replace("{{ Content }}",html)

    dir = os.path.dirname(dest_path)

    if not os.path.exists(dir):
        os.makedirs(dir)

    with open(file=dest_path,mode='w',encoding='utf-8') as writer:
        writer.write(new_html)
        writer.close()
        
    

main()
