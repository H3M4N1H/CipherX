"""Tests for hash identification and wordlist cracking."""

from cipherx.modules.hashing import cracker
from cipherx.modules.hashing.identifier import identify


def test_identify_md5():
    assert "MD5" in identify("5f4dcc3b5aa765d61d8327deb882cf99")


def test_identify_sha256():
    digest = "a" * 64
    assert "SHA256" in identify(digest)


def test_identify_bcrypt():
    bcrypt_hash = "$2b$" + "a" * 56
    assert "bcrypt" in identify(bcrypt_hash)


def test_identify_unknown():
    assert identify("not-a-hash") == []


def test_crack_known_md5():
    # md5("password")
    word, algo, source = cracker.crack("5f4dcc3b5aa765d61d8327deb882cf99")
    assert word == "password"
    assert algo == "md5"
    assert source == "wordlist"


def test_crack_miss_returns_none():
    word, algo, source = cracker.crack("0" * 32)
    assert word is None
    assert source is None
