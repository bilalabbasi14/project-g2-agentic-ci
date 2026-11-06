"""diff_reader tool: per-file view of an LRTS build diff (local file only).

File splitting and extension filtering follow parse_git_diff_by_file in
DANTE's git_utils.py: a new file starts at "diff --git a/", files whose
extension is in EXTENSIONS_TO_IGNORE_IN_DIFF (config.py) are skipped, and
changed lines are the +/- lines without the +++/--- headers.
"""
import os

# EXTENSIONS_TO_IGNORE_IN_DIFF from DANTE config.py
IGNORED_EXTENSIONS = {".xml", ".html", ".json", ".yaml", ".yml", ".properties", ".md", ".txt",
                      ".gitignore", ".gitattributes", ".dockerignore", ""}


def split_diff(raw_text, ignored_extensions=IGNORED_EXTENSIONS):
    """Return {path: {"hunk_text", "changed_lines", "added", "removed"}} for kept files."""
    files, current = {}, None
    for line in (raw_text or "").splitlines():
        if line.startswith("diff --git a/"):
            parts = line.split(" b/", 1)
            path = parts[1] if len(parts) == 2 else None
            if path is None or os.path.splitext(path)[1].lower() in ignored_extensions:
                current = None
            else:
                current = files.setdefault(path, {"lines": [], "changed": [], "added": 0, "removed": 0})
        if current is None:
            continue
        current["lines"].append(line)
        if line.startswith("+") and not line.startswith("+++"):
            current["changed"].append(line[1:])
            current["added"] += 1
        elif line.startswith("-") and not line.startswith("---"):
            current["changed"].append(line[1:])
            current["removed"] += 1
    return {p: {"hunk_text": "\n".join(f["lines"]), "changed_lines": "\n".join(f["changed"]),
                "added": f["added"], "removed": f["removed"]}
            for p, f in files.items() if f["changed"]}


class DiffReader:
    def __init__(self, diff_path, ignored_extensions=IGNORED_EXTENSIONS):
        with open(diff_path, "r", encoding="utf-8", errors="ignore") as f:
            self.files = split_diff(f.read(), ignored_extensions)

    @classmethod
    def from_files(cls, diff_files):
        """Serve list_files() and __call__(file) from an already-split diff
        (BuildData.diff_files, the output of split_diff); reads no file."""
        reader = cls.__new__(cls)
        reader.files = dict(diff_files)
        return reader

    def list_files(self):
        return sorted(self.files)

    def __call__(self, file):
        if file not in self.files:
            return {"file": file, "found": False}
        return {"file": file, "found": True, **self.files[file]}
