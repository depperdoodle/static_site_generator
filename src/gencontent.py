from markdown_blocks import markdown_to_html_node
import os
from pathlib import Path

def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return(line[2:]).strip()
    else:
        raise Exception("No Heading here, boss")
    
def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()
    html_string = markdown_to_html_node(markdown).to_html()
    template = template.replace("{{ Title }}", extract_title(markdown))
    template = template.replace("{{ Content }}", html_string)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    some_dir = os.path.dirname(dest_path)
    os.makedirs(some_dir, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
       from_path = os.path.join(dir_path_content, filename)
       dest_path = os.path.join(dest_dir_path, filename)
       if os.path.isfile(from_path):
           dest_path = Path(dest_path).with_suffix(".html")
           generate_page(from_path,template_path, dest_path, basepath)
       else:
           generate_pages_recursive(from_path, template_path, dest_path, basepath)