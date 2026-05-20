from __future__ import annotations

import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[3]
DOCS_ROOT = ROOT / "docs"

SKIP_PREFIXES = (
    "#",
    "http://",
    "https://",
    "mailto:",
    "tel:",
)


class DocsError(Exception):
    pass


def iter_markdown_link_targets(line: str) -> list[str]:
    targets: list[str] = []
    index = 0
    while index < len(line):
        label_start = line.find("[", index)
        if label_start == -1:
            break
        if label_start > 0 and line[label_start - 1] == "!":
            index = label_start + 1
            continue
        label_end = line.find("]", label_start + 1)
        if label_end == -1 or label_end + 1 >= len(line) or line[label_end + 1] != "(":
            index = label_start + 1
            continue

        target_start = label_end + 2
        if target_start < len(line) and line[target_start] == "<":
            target_end = line.find(">", target_start + 1)
            if target_end == -1 or target_end + 1 >= len(line) or line[target_end + 1] != ")":
                index = target_start + 1
                continue
            targets.append(line[target_start : target_end + 1])
            index = target_end + 2
            continue

        depth = 0
        position = target_start
        while position < len(line):
            char = line[position]
            if char == "\\":
                position += 2
                continue
            if char == "(":
                depth += 1
            elif char == ")":
                if depth == 0:
                    targets.append(line[target_start:position])
                    index = position + 1
                    break
                depth -= 1
            position += 1
        else:
            index = target_start
    return targets


def iter_markdown_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if ".venv" not in path.parts and ".git" not in path.parts
    )


def strip_link_suffix(raw_target: str) -> str:
    target = raw_target.strip()
    if not target or target.startswith(SKIP_PREFIXES):
        return ""
    if " " in target and not target.startswith("<"):
        # Markdown titles can follow a URL, e.g. (path "title").
        target = target.split(" ", maxsplit=1)[0]
    target = target.strip("<>")
    target = target.split("#", maxsplit=1)[0]
    target = target.split("?", maxsplit=1)[0]
    return unquote(target)


def check_internal_links() -> list[str]:
    errors: list[str] = []
    for markdown_path in iter_markdown_files():
        text = markdown_path.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            for raw_target in iter_markdown_link_targets(line):
                target = strip_link_suffix(raw_target)
                if not target:
                    continue
                target_path = (markdown_path.parent / target).resolve()
                try:
                    target_path.relative_to(ROOT)
                except ValueError:
                    errors.append(f"{markdown_path}:{line_number}: link escapes repo: {raw_target}")
                    continue
                if not target_path.exists():
                    errors.append(
                        f"{markdown_path}:{line_number}: broken internal link: {raw_target}"
                    )
    return errors


def check_docs_readme_indexes_all_docs() -> list[str]:
    readme = DOCS_ROOT / "README.md"
    if not readme.exists():
        return ["docs/README.md does not exist"]

    readme_text = readme.read_text(encoding="utf-8")
    errors: list[str] = []
    for doc_path in sorted(DOCS_ROOT.rglob("*.md")):
        if doc_path == readme:
            continue
        relative_path = doc_path.relative_to(DOCS_ROOT).as_posix()
        if relative_path not in readme_text:
            errors.append(f"docs/README.md does not index docs/{relative_path}")
    return errors


def main() -> int:
    errors = []
    errors.extend(check_internal_links())
    errors.extend(check_docs_readme_indexes_all_docs())

    if errors:
        print("Markdown documentation checks failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Markdown documentation checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
