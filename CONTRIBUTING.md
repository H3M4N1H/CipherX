# Contributing to CipherX

Thanks for your interest in improving CipherX! This project is a CTF
cipher/encoding auto-cracker intended for **educational and competition use
only**.

## Development setup

```bash
git clone https://github.com/H3M4N1H/CipherX.git
cd CipherX
python -m venv .venv && source .venv/bin/activate
make dev          # editable install with dev + optional deps, installs pre-commit
```

## Workflow

```bash
make fmt          # auto-format (black + ruff --fix)
make check        # lint + type-check + tests (mirror of CI)
```

All of the following must pass before a PR is merged — CI enforces them on
Python 3.10–3.13:

- `ruff check cipherx tests`
- `black --check cipherx tests`
- `mypy cipherx`
- `pytest`

## Adding a new decoder / cipher

1. Add the function to the appropriate module under `cipherx/modules/`.
2. Register it in that module's `ENCODERS` dict (encoders) or expose a
   `crack(...)` entry point (ciphers).
3. If it should participate in auto-detection, add a heuristic to
   `cipherx/core/detector.py`.
4. Add a round-trip test under `tests/`.

Decoders return the decoded `str` on success or `None` on failure — never
raise. Keep that contract: the layered cracker relies on it.

## Commit style

Keep commits focused and write a clear subject line. Reference an issue number
where one exists.

## Scope

CipherX is for authorized CTF and learning scenarios. Please don't submit
features whose only purpose is attacking systems you don't own.
