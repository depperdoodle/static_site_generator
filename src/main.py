from textnode import TextNode, TextType
import os
import shutil
from copystatic import clean_copy
from gencontent import generate_page, generate_pages_recursive

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")
    clean_copy("static", "public")
    generate_pages_recursive("content/", "template.html", "public/")


main()