"""Tests for experiments/build_devlog.py (P2-20): no data and no model needed."""
import pytest

from experiments.build_devlog import DevlogError, build, collect, demote_headings, read_entry


def _entry(folder, name, title, date, body="## Observed failure or limitation\n\ntext\n"):
    path = folder / name
    path.write_text(f"# {title}\n\nDate: {date}\nAuthor: Someone\n\n{body}", encoding="utf-8")
    return path


def test_entries_are_ordered_by_date_then_file_name(tmp_path):
    _entry(tmp_path, "2026-11-07-ali-b.md", "Second day", "2026-11-07")
    _entry(tmp_path, "2026-10-20-taha-z.md", "First day, later name", "2026-10-20")
    _entry(tmp_path, "2026-10-20-ali-a.md", "First day, earlier name", "2026-10-20")
    titles = [e.title for e in collect(tmp_path)]
    assert titles == ["First day, earlier name", "First day, later name", "Second day"]


def test_build_writes_contents_and_every_entry(tmp_path):
    entries = tmp_path / "devlog"
    entries.mkdir()
    _entry(entries, "2026-11-06-ali-cache.md", "Cache", "2026-11-06")
    _entry(entries, "2026-10-20-bilal-pins.md", "Pins", "2026-10-20")
    out = tmp_path / "devlog.md"
    build(entries, out)
    text = out.read_text(encoding="utf-8")
    assert text.startswith("# Development log")
    assert "1. [2026-10-20 — Pins](#2026-10-20-bilal-pins)" in text
    assert "2. [2026-11-06 — Cache](#2026-11-06-ali-cache)" in text
    assert text.index('<a id="2026-10-20-bilal-pins"></a>') < text.index('<a id="2026-11-06-ali-cache"></a>')
    assert "### Observed failure or limitation" in text      # entry headings are one level down
    assert text.count("## Pins") == 1 and text.count("## Cache") == 1


def test_headings_in_code_blocks_are_not_changed():
    text = "## Change\n```\n# a shell comment\n```\n### Detail"
    assert demote_headings(text) == "### Change\n```\n# a shell comment\n```\n#### Detail"


def test_entry_without_date_or_title_is_rejected(tmp_path):
    no_date = tmp_path / "no-date.md"
    no_date.write_text("# Title\n\nAuthor: X\n", encoding="utf-8")
    with pytest.raises(DevlogError, match="Date"):
        read_entry(no_date)
    no_title = tmp_path / "no-title.md"
    no_title.write_text("Date: 2026-11-06\n", encoding="utf-8")
    with pytest.raises(DevlogError, match="title"):
        read_entry(no_title)


def test_bold_date_line_is_accepted(tmp_path):
    path = tmp_path / "e.md"
    path.write_text("# T\n\n**Date:** 2026-11-08\n", encoding="utf-8")
    assert read_entry(path).date == "2026-11-08"
