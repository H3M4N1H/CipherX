"""Tests for cipher modules (Caesar, Vigenere, XOR)."""

from cipherx.modules.ciphers import caesar, vigenere, xor


def test_caesar_decrypt_known_shift():
    # "Khoor" is "Hello" shifted by +3
    assert caesar.decrypt("Khoor", 3) == "Hello"


def test_caesar_brute_force_count():
    results = caesar.brute_force("Khoor")
    assert len(results) == 25
    assert ("Hello" in [d for _, d in results]) or any(d == "Hello" for _, d in results)


def test_caesar_crack_with_flag_format():
    cipher = caesar.decrypt("HTB{caesar}", -5)  # encrypt by shifting +5
    decoded, method = caesar.crack(cipher, flag_format="HTB{")
    assert decoded == "HTB{caesar}"
    assert "Caesar" in method


def test_vigenere_roundtrip():
    key = "lemon"
    plaintext = "attackatdawn"
    # Encrypt by using the negative-shift property: encrypt == decrypt with inverse.
    # Build ciphertext by encrypting manually.
    encrypted = _vigenere_encrypt(plaintext, key)
    assert vigenere.decrypt(encrypted, key) == plaintext


def test_vigenere_crack_from_wordlist():
    plaintext = "HTB{vigenere_key_secret}"
    encrypted = _vigenere_encrypt(plaintext, "secret")
    decoded, method = vigenere.crack(encrypted, flag_format="HTB{")
    assert decoded == plaintext
    assert "secret" in method


def test_xor_single_byte_roundtrip():
    data = b"HTB{xor_me}"
    xored = xor.decrypt_single(data, 0x42)
    decoded, method = xor.crack_single(xored.hex(), flag_format="HTB{")
    assert decoded == "HTB{xor_me}"
    assert "0x42" in method


def test_xor_multibyte_roundtrip():
    data = b"secret message"
    key = "key"
    xored = xor.decrypt_multibyte(data, key)
    decoded, _ = xor.crack_multibyte(xored.hex(), key)
    assert decoded == "secret message"


def _vigenere_encrypt(text, key):
    key = key.lower()
    out = []
    ki = 0
    for c in text:
        if c.isalpha():
            base = ord("A") if c.isupper() else ord("a")
            shift = ord(key[ki % len(key)]) - ord("a")
            out.append(chr((ord(c) - base + shift) % 26 + base))
            ki += 1
        else:
            out.append(c)
    return "".join(out)
