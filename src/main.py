from textnode import TextNode, TextType
import os
import shutil
from copystatic import clean_copy
from gencontent import generate_page, generate_pages_recursive
import sys


def main():
    if os.path.exists("docs"):
        shutil.rmtree("docs")
    os.mkdir("docs")
    clean_copy("static", "docs")
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    generate_pages_recursive("content/", "template.html", "docs", basepath)
    
    
main()