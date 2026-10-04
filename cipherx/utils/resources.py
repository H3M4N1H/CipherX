"""Locate packaged data files (wordlists) in a way that works whether CipherX
is run from a source checkout, an editable install, or a built wheel."""

from __future__ import annotations

import os
from importlib import resources
from pathlib import Path

_ENV_WORDLIST = "CIPHERX_WORDLIST"


def wordlist_path(name: str) -> Path:
    """Return the filesystem path to a bundled wordlist by file name.

    For ``rockyou_mini.txt.gz`` the ``CIPHERX_WORDLIST`` environment variable,
    when set, overrides the bundled list so users can point at a full wordlist.
    """
    if name == "rockyou_mini.txt.gz":
        override = os.environ.get(_ENV_WORDLIST)
        if override:
            return Path(override).expanduser()
    return Path(str(resources.files("cipherx") / "wordlists" / name))
