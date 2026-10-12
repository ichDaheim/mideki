import re
from pathlib import Path

import mideki
from mideki import check_golden, output_fingerprint, token_map_sha256

CHANGELOG = Path(__file__).resolve().parent.parent / 'CHANGELOG.md'


def _changelog_section(version: str) -> str:
    text = CHANGELOG.read_text(encoding='utf-8')
    match = re.search(rf'^## {re.escape(version)}\b.*?(?=^## |\Z)', text, flags=re.M | re.S)
    assert match, f'CHANGELOG.md has no section for version {version}'
    return match.group(0)


def test_golden_output_unchanged():
    # A failure means the phoneme output changed. If intended: run
    # `mideki-check-golden --update`, bump the MINOR version, add a CHANGELOG entry.
    mismatches = check_golden()
    assert not mismatches, '\n'.join(mismatches)


def test_changelog_records_current_fingerprints():
    section = _changelog_section(mideki.__version__)
    assert output_fingerprint() in section, 'output changed: bump the MINOR version and record the new fingerprint'
    assert token_map_sha256() in section
