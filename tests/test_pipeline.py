"""Tests for detector, layered cracker, and reporter."""

import json

from cipherx.core.detector import detect
from cipherx.core.layered import crack_layers
from cipherx.core.reporter import Reporter


def test_detect_hex():
    names = [name for name, _ in detect("48656c6c6f20576f726c64")]
    assert "Hex" in names


def test_detect_base64():
    names = [name for name, _ in detect("SGVsbG8gV29ybGQ=")]
    assert "Base64" in names


def test_detect_md5_hash():
    names = [name for name, _ in detect("5f4dcc3b5aa765d61d8327deb882cf99")]
    assert "MD5 Hash" in names


def test_detect_sorted_by_confidence():
    results = detect("01001000 01101001")
    confidences = [c for _, c in results]
    assert confidences == sorted(confidences, reverse=True)


def test_crack_layers_multi_layer():
    # Hex -> Base64 -> ROT13 -> HTB{multi_layer_test}
    payload = "565564506533706f6557643258336c7562484a6c583264795a6d6439"
    result, chain, found = crack_layers(payload, flag_format="HTB{", max_layers=5)
    assert found is True
    assert result == "HTB{multi_layer_test}"
    assert chain == ["Hex", "Base64", "ROT13"]


def test_crack_layers_single_base64():
    result, chain, found = crack_layers("SGVsbG8gV29ybGQ=", flag_format="Hello", max_layers=3)
    assert found is True
    assert result == "Hello World"


def test_reporter_json_roundtrip(tmp_path):
    reporter = Reporter("input", "HTB{flag}", ["Hex", "Base64"], True, "HTB{")
    out = tmp_path / "report.json"
    reporter.to_json(str(out))
    data = json.loads(out.read_text())
    assert data["output"] == "HTB{flag}"
    assert data["layers"] == 2
    assert data["flag_found"] is True


def test_reporter_html_contains_flag(tmp_path):
    reporter = Reporter("input", "HTB{flag}", ["Hex"], True, "HTB{")
    out = tmp_path / "report.html"
    reporter.to_html(str(out))
    html = out.read_text()
    assert "HTB{flag}" in html
    assert "FLAG FOUND" in html
