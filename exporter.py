import os
import shutil

import pdfkit
from PIL import Image

source_folder = "your/source/folder"
target_folder = "your/target/folder"


def ensure_dir_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def move_and_convert(relative_path, filename):
    source_file_path = os.path.join(source_folder, relative_path, filename)
    target_path = os.path.join(target_folder, relative_path)
    ensure_dir_exists(target_path)

    if filename.endswith(".pdf"):
        shutil.copy(source_file_path, target_path)
    elif filename.endswith(".html"):
        pdf_path = os.path.join(target_path, filename.replace(".html", ".pdf"))
        pdfkit.from_file(source_file_path, pdf_path)
    elif filename.endswith((".png", ".jpg", ".jpeg", ".bmp")):
        image = Image.open(source_file_path)
        pdf_path = os.path.join(target_path, filename.rsplit(".", 1)[0] + ".pdf")
        image.save(pdf_path, "PDF", resolution=100.0)
    else:
        new_path = os.path.join(target_path, filename)
        shutil.move(source_file_path, new_path)


def process_directory(root, relative_path=""):
    for item in os.listdir(root):
        item_path = os.path.join(root, item)
        if os.path.isdir(item_path):
            process_directory(item_path, os.path.join(relative_path, item))
        elif os.path.isfile(item_path):
            move_and_convert(relative_path, item)


process_directory(source_folder)
