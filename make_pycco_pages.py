import argparse
from pathlib import Path
from shutil import rmtree

import pycco


def main(exclude):
    """
    Generate Pycco HTML file tree out of a specific subset of sources. The
    subset is controlled by expliciti include and exclude patterns.
    """
    build_dest = Path('./pages')
    if build_dest.exists():
        rmtree(build_dest)
    build_dest.mkdir()

    all_exclude = Path('.gitignore').read_text().splitlines()
    all_exclude.extend(['.git', '.gitignore', '.github'])
    all_exclude.extend(exclude)

    source_files = find_files(include=["*.py"], exclude=all_exclude)

    pycco.process(
        sources=[str(f) for f in source_files],
        outdir=str(build_dest),
        index=True
    )


def find_files(path=Path('.'), include=[], exclude=[]):
    """
    Find all files in a path that match one of the include patterns while not
    matching any of the exclude patterns at any level.
    """
    for item in path.iterdir():
        # Exclude some files and dirs
        if any(item.match(pattern) for pattern in exclude):
            continue

        if item.is_dir():
            # Recursively look for files
            yield from find_files(item, include, exclude)
        else:
            # See if any files match the include patterns
            if any(item.match(pattern) for pattern in include):
                yield item


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--exclude", help="Comma separated list of file patterns to exclude")
    args = parser.parse_args()

    exclude = args.exclude.split(',') if args.exclude else []
    main(exclude)
