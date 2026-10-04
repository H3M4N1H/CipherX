"""Tests for the encoding/decoding primitives."""

import pytest

from cipherx.modules.encoding import base, misc
from cipherx.modules.encoding import hex as hexmod


@pytest.mark.parametrize(
    "func,encoded,expected",
    [
        (base.decode_base64, "SGVsbG8gV29ybGQ=", "Hello World"),
        (base.decode_base64, "SGVsbG8h", "Hello!"),  # aligned length (padding-bug regression)
        (base.decode_base64_urlsafe, "SGVsbG8h", "Hello!"),
        (base.decode_base32, "JBSWY3DP", "Hello"),
        (base.decode_base85, "NM&qnZv", "Hello"),
        (base.decode_base16, "48656C6C6F", "Hello"),
        (hexmod.decode_hex, "48656c6c6f", "Hello"),
        (hexmod.decode_hex, "0x48 0x65", "He"),
        (hexmod.decode_hex_spaced, "48 65 6c 6c 6f", "Hello"),
        (hexmod.decode_url, "Hello%20World%21", "Hello World!"),
        (hexmod.decode_url_plus, "Hello+World", "Hello World"),
        (hexmod.decode_html_entities, "&lt;a&gt;", "<a>"),
        (hexmod.decode_decimal, "72 101 108 108 111", "Hello"),
        (misc.decode_rot13, "Uryyb", "Hello"),
        (misc.decode_binary, "01001000 01101001", "Hi"),
        (misc.decode_octal, "110 145", "He"),
        (misc.decode_morse, ".... .. / - .... . .-. .", "HI THERE"),
        (misc.decode_atbash, "Svool", "Hello"),
        (misc.decode_reversed, "olleH", "Hello"),
    ],
)
def test_decoders(func, encoded, expected):
    assert func(encoded) == expected


def test_base58_roundtrip():
    # "Hello World" in Base58 (Bitcoin alphabet)
    assert base.decode_base58("JxF12TrwUP45BMd") == "Hello World"


def test_rot13_is_involutive():
    text = "The quick brown fox"
    assert misc.decode_rot13(misc.decode_rot13(text)) == text


def test_binary_rejects_non_binary():
    assert misc.decode_binary("hello") is None


def test_decoders_return_none_on_garbage():
    assert hexmod.decode_hex("zzzz") is None
    assert hexmod.decode_decimal("not numbers") is None
