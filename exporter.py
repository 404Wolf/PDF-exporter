import argparse
import os
import subprocess
import shutil
from PIL import Image


def ensure_dir_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def move_and_convert(relative_path, filename, source_folder, target_folder):
    source_file_path = os.path.join(source_folder, relative_path, filename)
    target_path = os.path.join(target_folder, relative_path)
    ensure_dir_exists(target_path)

    if filename.endswith(".pdf"):
        shutil.copy(source_file_path, target_path)
    elif filename.endswith((".html")):
        pdf_path = os.path.join(target_path, filename.replace(".html", ".pdf"))
        subprocess.run(["pandoc", source_file_path, "-o", pdf_path])
    elif filename.endswith(('.html', '.json', '.yml', '.yaml', '.txt', '.md', '.csv')):
        image = Image.open(source_file_path)
        pdf_path = os.path.join(target_path, filename.rsplit(".", 1)[0] + ".pdf")
        image.save(pdf_path, "PDF", resolution=100.0)
    else:
        new_path = os.path.join(target_path, filename)
        print(f"Skipping {new_path}")


def process_directory(
    source_folder: str, target_folder: str, root: str, relative_path: str = ""
):
    for item in os.listdir(root):
        item_path = os.path.join(root, item)
        if os.path.isdir(item_path):
            process_directory(
                source_folder,
                target_folder,
                item_path,
                os.path.join(relative_path, item),
            )
        elif os.path.isfile(item_path):
            move_and_convert(relative_path, item, source_folder, target_folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Move and convert files while preserving folder structure."
    )
    parser.add_argument("source_folder", type=str, help="Source folder path.")
    parser.add_argument("target_folder", type=str, help="Target folder path.")
    args = parser.parse_args()

    process_directory(args.source_folder, args.target_folder, args.source_folder)
