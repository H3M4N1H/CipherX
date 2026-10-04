"""Tests for scoring/entropy helpers."""

from cipherx.utils.helpers import contains_flag, entropy, score_output


def test_entropy_empty():
    assert entropy("") == 0


def test_entropy_uniform_higher_than_repeated():
    assert entropy("ABCDEFGH") > entropy("AAAAAAAA")


def test_contains_flag_literal():
    assert contains_flag("here is HTB{found}", "HTB{")
    assert not contains_flag("nothing here", "HTB{")


def test_contains_flag_regex():
    assert contains_flag("CTF{abc}", r"CTF\{.*\}")


def test_contains_flag_autodetect():
    assert contains_flag("flag{auto}", None)
    assert not contains_flag("plain text", None)


def test_score_flag_pattern_scores_high():
    score, reasons = score_output("HTB{a_real_flag}")
    assert score >= 6
    assert any("Flag-like" in r for r in reasons)


def test_score_encoded_blob_scores_low():
    score, _ = score_output("4A6B2F8D9E1C3A5B7F0E==")
    assert score < 6
