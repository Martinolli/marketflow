from __future__ import annotations

import subprocess
import sys
from email.parser import Parser
from pathlib import Path

from packaging.requirements import Requirement


REPO_ROOT = Path(__file__).resolve().parents[1]
REQUIREMENTS = REPO_ROOT / "requirements.txt"
SETUP_PY = REPO_ROOT / "setup.py"


def _requirement_lines() -> list[str]:
    lines: list[str] = []
    for raw_line in REQUIREMENTS.read_text(encoding="utf-8").splitlines():
        stripped = raw_line.strip()
        if stripped and not stripped.startswith("#"):
            lines.append(stripped)
    return lines


def test_requirements_lines_are_parseable():
    for line in _requirement_lines():
        Requirement(line)


def test_requirements_loader_ignores_comments_and_blank_lines(tmp_path, monkeypatch):
    sample = tmp_path / "requirements.txt"
    sample.write_text("\n# comment\nrequests==2.32.3\n\npandas==2.2.3\n", encoding="utf-8")
    monkeypatch.syspath_prepend(str(REPO_ROOT))

    import setup

    assert setup.load_requirements(str(sample)) == ["requests==2.32.3", "pandas==2.2.3"]


def test_requirements_loader_does_not_silently_fallback(tmp_path, monkeypatch):
    monkeypatch.syspath_prepend(str(REPO_ROOT))

    import setup

    missing = tmp_path / "missing-requirements.txt"
    try:
        setup.load_requirements(str(missing))
    except FileNotFoundError:
        pass
    else:
        raise AssertionError("missing requirements.txt must fail instead of generating fallback metadata")


def test_setup_py_does_not_embed_quoted_list_metadata_syntax():
    source = SETUP_PY.read_text(encoding="utf-8")
    assert 'Requires-Dist:' not in source
    assert '- "' not in source


def test_generated_metadata_requires_dist_entries_parse(tmp_path):
    subprocess.run(
        [sys.executable, "setup.py", "egg_info", "--egg-base", str(tmp_path)],
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    pkg_info = tmp_path / "marketflow.egg-info" / "PKG-INFO"
    metadata = Parser().parsestr(pkg_info.read_text(encoding="utf-8"))
    requirements = metadata.get_all("Requires-Dist") or []

    assert len(requirements) == len(_requirement_lines())
    for requirement in requirements:
        assert not requirement.lstrip().startswith("-")
        assert '"' not in requirement
        Requirement(requirement)


def test_generated_packaging_artifacts_are_ignored_by_git():
    result = subprocess.run(
        ["git", "check-ignore", "marketflow.egg-info", "build/", "dist/"],
        cwd=REPO_ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    assert result.returncode == 0
    assert set(result.stdout.splitlines()) == {"marketflow.egg-info", "build/", "dist/"}


def test_no_generated_packaging_directory_is_tracked():
    result = subprocess.run(
        ["git", "ls-files", "marketflow.egg-info", "*.dist-info", "build", "dist"],
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    assert result.stdout.strip() == ""
