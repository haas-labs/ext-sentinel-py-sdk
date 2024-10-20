#!/usr/bin/env python3

import pathlib

DOCS_DIR = pathlib.Path("docs")
DEFAULT_INDENT = "  "
IGNORE_LIST = ["docs/.obsidian", "docs/SUMMARY.md", "docs/README.md"]


def generate_summary(path: pathlib.Path, indent_level: int = 0):
    indent = "  " * indent_level
    items = sorted(path.glob("*"))
    for item in items:
        if str(item) in IGNORE_LIST:
            continue

        # if the item is directory, process it recursively
        if item.is_dir(follow_symlinks=False):
            print(f"{indent}- [{str(item.name)}](#)")
            generate_summary(item, indent_level=indent_level + 1)
        else:
            print(f"{indent}- [{item.stem}]({item.relative_to(DOCS_DIR)})")
    # for filepath in path.glob("**/*md"):
    #     rel_filepath = pathlib.Path(str(filepath).replace(str(path), ""))

    #     if str(rel_filepath.parent) == "/":
    #         print(f"- [{rel_filepath.stem}]({rel_filepath})")
    #     else:
    #         name = os.sep.join([str(rel_filepath.parent), str(rel_filepath.stem)])
    #         print(f"- [{name}]({rel_filepath})")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(prog="generate-docs-summary")
    parser.add_argument("--path", type=pathlib.Path, required=True, help="Path to documentation")
    args = parser.parse_args()

    readme_path: pathlib.Path = args.path / "README.md"
    if readme_path.exists():
        print("- [Introduction](README.md)")

    generate_summary(args.path)
