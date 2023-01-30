import argparse, os, json
from pathlib import Path
from typing import List
from collections import OrderedDict
from PIL import Image
from pillow_heif import register_heif_opener
from jinja2 import Environment, FileSystemLoader

register_heif_opener()

OUTPUT_DIR = Path("./dist")
OUTPUT_GALLERY_DIR = Path("./dist/images")
SEARCH_GLOB_PATTERNS = [
    "**/*.[jJ][pP]?[gG]",
    "**/*.[hH][eE][iI][cC]",
    "**/*.[pP][nN][gG]",
]
TEMPLATE_ROOT_DIR = Path("./src/template/html/")
environment = Environment(loader=FileSystemLoader(TEMPLATE_ROOT_DIR))
template = environment.get_template("index.html")


def make_thumbnail(image_path, thmb_path):
    print(f"Creating thumbnail for {image_path}")
    with Image.open(image_path) as image:
        image.thumbnail((350, 350))
        image.save(thmb_path, format="webp")


def get_file_list(inputdir) -> List[Path]:
    output_list = []
    for pattern in SEARCH_GLOB_PATTERNS:
        for f in inputdir.glob(pattern):
            output_list.append(Path(f))
    return sorted(output_list)


def main():
    parser = argparse.ArgumentParser(
        description="This command will output a web gallery HTML file"
    )
    parser.add_argument(
        "inputdir",
        action="store",
        type=str,
        help="Path to directory containing gallery images",
    )

    args = parser.parse_args()
    input_path = Path(args.inputdir)
    gallery_data = OrderedDict()
    for source_file_path in get_file_list(input_path):
        print(f"Processing {source_file_path}")
        target_thmb_path = source_file_path.parent.joinpath(
            ".thmb", source_file_path.name
        ).with_suffix(".webp")

        if target_thmb_path.exists():
            print(f"Found existing thumbnail: {target_thmb_path}")
        else:
            target_thmb_path.parent.mkdir(parents=True, exist_ok=True)
            make_thumbnail(source_file_path, target_thmb_path)

        relative_file_path = source_file_path.relative_to(input_path)
        relative_thmb_path = target_thmb_path.relative_to(input_path)
        relative_root_dir_path = relative_file_path.parent

        if str(relative_root_dir_path) not in gallery_data:
            gallery_data[str(relative_root_dir_path)] = []

        gallery_data[str(relative_root_dir_path)].append(
            {
                "image_path": relative_file_path,
                "thumbnail_path": relative_thmb_path,
            }
        )

    content = template.render(gallery=gallery_data)
    output_file_path = OUTPUT_DIR.joinpath("index.html")
    with open(output_file_path, mode="w", encoding="utf-8") as message:
        message.write(content)
        print(f"... wrote {output_file_path}")

    manifest_file_path = OUTPUT_DIR.joinpath("manifest.json")
    with open(manifest_file_path, mode="w", encoding="utf-8") as message:
        json_data = json.dumps(gallery_data, default=lambda o: str(o), indent=4)
        message.write(json_data)
        print(f"... wrote {manifest_file_path}")


if __name__ == "__main__":
    main()
