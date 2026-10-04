# 🔓 CipherX

[![CI](https://github.com/Dreadonyx/CipherX/actions/workflows/ci.yml/badge.svg)](https://github.com/Dreadonyx/CipherX/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A multi-layer CTF cipher/encoding auto-cracker for your terminal. Give it a
ciphertext — it figures out the encoding stack and peels it layer by layer
until it finds your flag.

```
Input: 565564506533706f6557643258336c7562484a6c583264795a6d6439
  Layer 1: Hex     → VUdPe3poeWd2X3lubHJlX2dyZmd9
  Layer 2: Base64  → UGO{zhygv_ynlre_grfg}
  Layer 3: ROT13   → HTB{multi_layer_test}

✅ FLAG FOUND: HTB{multi_layer_test}
[Chain] Hex → Base64 → ROT13
```

---

## ⚙️ Installation

```bash
git clone https://github.com/Dreadonyx/CipherX.git
cd CipherX

# core install (encodings, ciphers, hashing)
pip install .

# everything (AES + steganography + online hash lookup)
pip install ".[full]"
```

Optional extras, if you only want some capabilities:

| Extra     | Enables                               |
|-----------|---------------------------------------|
| `crypto`  | AES CBC/ECB decryption (pycryptodome) |
| `steg`    | LSB image extraction (Pillow)         |
| `online`  | Online hash lookup (requests)         |
| `full`    | all of the above                      |

---

## 🚀 Usage

After install, use the `cipherx` command (or `python -m cipherx`).

### Auto-crack mode
```bash
# Auto-detect and crack up to 3 layers
cipherx -a "SGVsbG8gV29ybGQ="

# With flag format (stops as soon as the flag is found)
cipherx -a "565564506533..." --flag-format "HTB{" --layers 5

# From a file
cipherx -f cipher.txt --flag-format "CTF{"

# Save a report
cipherx -a "..." --flag-format "HTB{" --report html
```

### Interactive menu
```bash
cipherx -i
```

### Just detect encoding type
```bash
cipherx -d "SGVsbG8="
```

---

## 🧩 Supported Techniques

### Encodings (auto-detected + manual)
| Encoding | Notes |
|----------|-------|
| Base64 / Base64 URL-safe | With auto padding fix |
| Base32 / Base58 / Base85 / Base16 | All variants |
| Hex | With/without spaces, 0x prefix |
| URL Encoding | %xx and + variants |
| HTML Entities | `&amp;` `&#x41;` etc |
| Binary | Space or 8-char grouped |
| Octal | Space-separated |
| Decimal ASCII | Space-separated decimal values |
| ROT13 / ROT47 | Classic rotations |
| Atbash | A↔Z mirror cipher |
| Morse Code | Dot-dash with spaces |
| Reversed | String reversal |

### Ciphers
| Cipher | Method |
|--------|--------|
| Caesar | Brute forces all 25 shifts |
| Vigenere | Wordlist-based key attack |
| XOR (single-byte) | Brute forces 0x00–0xFF |
| XOR (multi-byte) | Known key decryption |
| AES CBC/ECB | Known key + IV decryption |

### Hashing
| Feature | Detail |
|---------|--------|
| Hash identification | MD5, SHA1, SHA256, SHA512, bcrypt, NTLM... |
| Wordlist crack | Against the bundled mini wordlist |
| Online lookup | md5decrypt.net (optional, needs `online` extra) |

### Steganography
| Feature | Detail |
|---------|--------|
| LSB extraction | From PNG/JPG images (needs `steg` extra) |
| Strings extraction | Like `strings` — extracts printable content + flags |

---

## 🧠 How Auto-Detection Works

CipherX uses two signals to decide when it's done:

**1. Flag Format Match** — if you provide `--flag-format "HTB{"`, it stops the
moment the decoded output contains it.

**2. Entropy + Printability Scoring** — when no flag format is given, each
decoded layer is scored:
- Fully printable ASCII → +3
- Contains common words → +2
- Entropy dropped significantly → +2
- Flag-like pattern `XX{...}` detected → +5
- Still looks encoded → −1 to −3

Score ≥ 6 = plaintext found. Below threshold = keep decoding.

---

## 📖 Wordlists

CipherX ships a **curated mini** rockyou list (the most common passwords) so
hash cracking works out of the box without a 50 MB download. To crack against a
full wordlist, point the `CIPHERX_WORDLIST` environment variable at a gzipped
list:

```bash
export CIPHERX_WORDLIST=/path/to/rockyou.txt.gz
cipherx -i   # option 5 → hash crack
```

---

## 📁 Project Structure

```
CipherX/
├── cipherx/
│   ├── cli.py                 # Command-line entry point
│   ├── __main__.py            # `python -m cipherx`
│   ├── core/
│   │   ├── detector.py        # Auto-detect encoding type
│   │   ├── layered.py         # Multi-layer recursive cracker
│   │   ├── interactive.py     # Interactive menu
│   │   └── reporter.py        # JSON + HTML reports
│   ├── modules/
│   │   ├── encoding/          # Base*, Hex, URL, ROT, Binary, Morse...
│   │   ├── hashing/           # Hash identify + wordlist/online crack
│   │   ├── ciphers/           # Caesar, Vigenere, XOR, AES
│   │   └── steg/              # LSB + strings extraction
│   ├── utils/                 # Logger, scoring/entropy helpers, resources
│   └── wordlists/             # Bundled mini wordlists
├── tests/                     # pytest suite
├── pyproject.toml
└── .github/workflows/ci.yml
```

---

## 🧪 Try It

```bash
# Single layer Base64
cipherx -a "SGVsbG8gV29ybGQ=" --flag-format "Hello"

# 3-layer: Hex → Base64 → ROT13
cipherx -a "565564506533706f6557643258336c7562484a6c583264795a6d6439" --flag-format "HTB{" --layers 5

# Hash crack (interactive: option 5 → 5f4dcc3b5aa765d61d8327deb882cf99 → "password")
cipherx -i
```

---

## 🛠️ Development

```bash
make dev      # editable install with dev + full extras + pre-commit
make check    # ruff + mypy + pytest (what CI runs)
make fmt      # auto-format
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 👤 Author

**Dreadonyx** — [github.com/Dreadonyx](https://github.com/Dreadonyx)

> ⚠️ For CTF and educational use only.
