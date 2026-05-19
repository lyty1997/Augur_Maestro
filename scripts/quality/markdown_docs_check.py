from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
DOCS_ROOT = ROOT / "docs"

MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
SKIP_PREFIXES = (
    "#",
    "http://",
    "https://",
    "mailto:",
    "tel:",
)


class DocsError(Exception):
    pass


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
            for raw_target in MARKDOWN_LINK_RE.findall(line):
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
