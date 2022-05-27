import argparse
from pathlib import Path
import pdb

SEARCH_GLOB_PATTERN = "*.thmb.jpg"
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


def get_file_list(inputdir):
    search_path = Path(inputdir)
    file_list = search_path.glob(SEARCH_GLOB_PATTERN)
    return [Path(f).relative_to('./html/') for f in sorted(file_list)]


def render_gallery_html(filepath):
    parameter_list = (
        str(filepath),                           # Relative path to thumbnail
        filepath.name.replace('.thmb.jpg', ''),  # File basename without suffix
        str(filepath).replace('thmb.', ''),      # Full size file path
        filepath.name.replace('.thmb.jpg', ''),  # File basename without suffix
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

    for filepath in get_file_list(args.inputdir):
        html_string = render_gallery_html(filepath)
        print(html_string)


if __name__ == "__main__":
    main()
