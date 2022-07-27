import argparse
from pathlib import Path
import shutil
from PIL import Image

OUTPUT_DIR = Path("./dist")
OUTPUT_GALLERY_DIR = Path("./dist/images")
SEARCH_GLOB_PATTERN = "*.jpg"
TEMPLATE_ROOT_DIR = Path("./src/template/html/")
TEMPLATE_HTML = """
                <div class="col">
                    <div class="card shadow-sm">
                        <img src="%s" class="card-img-top" alt="%s">
                        <div class="card-body">
                            <div class="d-flex justify-content-between align-items-center">
                                <div class="btn-group">
                                    <a href="%s" role="button" class="btn btn-primary btn-sm" target="_blank" download>Download</a>
                                </div>
                                <small class="text-muted">%s</small>
                            </div>
                        </div>
                    </div>
                </div>
"""


def make_thumbnail(image_path, thmb_path):
    with Image.open(image_path) as image:
        image.thumbnail((350, 350))
        image.save(thmb_path)


def get_file_list(inputdir):
    search_path = Path(inputdir)
    file_list = search_path.glob(SEARCH_GLOB_PATTERN)
    return [Path(f) for f in sorted(file_list)]


def render_gallery_html(filepath):
    # TODO: Render paths relative to dist
    filepath = filepath.relative_to(OUTPUT_DIR)
    parameter_list = (
        str(filepath),  # Relative path to thumbnail
        filepath.name.replace("thmb_", ""),  # File basename without prefix
        str(filepath).replace("thmb_", ""),  # Full size file path
        filepath.name.replace("thmb_", ""),  # File basename without suffix
    )
    return TEMPLATE_HTML % parameter_list


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

    html_gallery_string = ""
    for filepath in get_file_list(args.inputdir):
        target_path = OUTPUT_GALLERY_DIR.joinpath(filepath.name)
        thmb_path = OUTPUT_GALLERY_DIR.joinpath("thmb_" + filepath.name)

        shutil.copy(filepath, target_path)
        make_thumbnail(filepath, thmb_path)
        html_gallery_string += render_gallery_html(thmb_path)

    with open(TEMPLATE_ROOT_DIR.joinpath("index.html"), "rt") as fin:
        with open(OUTPUT_DIR.joinpath("index.html"), "wt") as fout:
            for line in fin:
                fout.write(line.replace("{{GALLERY}}", html_gallery_string))


if __name__ == "__main__":
    main()
