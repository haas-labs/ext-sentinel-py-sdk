#!/usr/bin/env python3

import os
import pathlib


def generate_summary(path: pathlib.Path):
    for filepath in path.glob("**/*md"):
        rel_filepath = pathlib.Path(str(filepath).replace(str(path), ""))

        if str(rel_filepath.parent) == "/":
            print(f"- [{rel_filepath.stem}]({rel_filepath})")
        else:
            name = os.sep.join([str(rel_filepath.parent), str(rel_filepath.stem)])
            print(f"- [{name}]({rel_filepath})")

        # name = name
        # print(name, rel_filepath)

        # level = rel_filepath.count(os.sep)
        # indent = " " * 2 * level
        # summary_lines.append(f"{indent}* [{filepath.name}]({rel_filepath})")
        # print(structure, rel_filepath)
    # for root, dirs, files in os.walk(start_path):
    # Adjust the depth level based on the root directory
    #     for f in sorted(files):
    #         if f.endswith(".md"):
    #             rel_path = os.path.relpath(os.path.join(root, f), start_path)
    #             summary_lines.append(f"{indent}* [{f}](./{rel_path})\n")

    # with open(os.path.join(start_path, 'SUMMARY.md'), 'w') as summary_file:
    #     summary_file.writelines(summary_lines)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(prog="generate-docs-summary")
    parser.add_argument("--path", type=pathlib.Path, required=True, help="Path to documentation")
    args = parser.parse_args()

    generate_summary(args.path)
