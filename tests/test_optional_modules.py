"""Tests for optional-dependency modules: AES (pycryptodome), steg (Pillow)."""

import pytest

from cipherx.modules.steg import strings


def test_strings_extracts_flag(tmp_path):
    f = tmp_path / "blob.bin"
    f.write_bytes(b"\x00\x01garbage\xffHTB{found_in_strings}\x00more")
    found, flags, err = strings.extract_from_file(str(f), flag_format="HTB{")
    assert err is None
    assert any("HTB{found_in_strings}" in s for s in flags)


def test_strings_min_length(tmp_path):
    f = tmp_path / "blob.bin"
    f.write_bytes(b"ab\x00longenoughstring\x00")
    found, _, err = strings.extract_from_file(str(f), min_length=4)
    assert err is None
    assert "longenoughstring" in found
    assert "ab" not in found  # shorter than min_length


aes = pytest.importorskip("cipherx.modules.ciphers.aes")
Crypto = pytest.importorskip("Crypto")


def test_aes_cbc_roundtrip():
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad

    from cipherx.modules.ciphers.aes import decrypt

    key = b"0123456789abcdef"
    iv = b"abcdef9876543210"
    plaintext = b"HTB{aes_cbc_mode}"
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = cipher.encrypt(pad(plaintext, AES.block_size))

    result, err = decrypt(ct.hex(), key.decode(), iv.hex(), "CBC")
    assert err is None
    assert result == "HTB{aes_cbc_mode}"


def test_aes_rejects_bad_key_length():
    from cipherx.modules.ciphers.aes import decrypt

    result, err = decrypt("deadbeef", "shortkey", None, "ECB")
    assert result is None
    assert "key length" in err.lower()
