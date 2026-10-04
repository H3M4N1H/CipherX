# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-10-04

First packaged release.

### Added
- Installable `cipherx` package with a `cipherx` console entry point and
  `python -m cipherx` support.
- `pyproject.toml` with optional extras: `crypto` (AES), `steg` (LSB),
  `online` (hash lookup), `full`, and `dev`.
- Test suite (`pytest`) covering encodings, ciphers, hashing, scoring,
  detection, the layered pipeline, and the reporter.
- GitHub Actions CI across Python 3.10–3.13 running ruff, black, mypy, pytest.
- Tooling config: ruff, black, mypy, pre-commit, Makefile.
- `CONTRIBUTING.md` and this changelog.
- `CIPHERX_WORDLIST` environment variable to point hash cracking at a full
  wordlist.
- A real `vigenere_keys.txt` wordlist (previously referenced but missing).

### Changed
- Restructured the flat layout into the `cipherx/` package.
- Replaced the mislabeled 53 MB "mini" rockyou (the full list) with a genuine
  curated mini wordlist; the full list is no longer tracked in git.
- `requests` is now an optional import; online lookup degrades gracefully when
  it is not installed.
- Minimum supported Python is now 3.10 (3.9 is end-of-life).

### Fixed
- Base64/Base32 padding bug that appended a full block of `=` to inputs whose
  length was already aligned.
