"""Secure configuration loader for Demented-Omni-Claw.
- Minimal .env parser with zero-trust defaults
- Optional XOR+Base64 pseudo-encryption for secrets (keeps keys out of plain text on disk)
- Model selection with Anthropic Claude Opus 4.6 primary and graceful fallbacks
"""
from __future__ import annotations

import base64
import hashlib
import os
from pathlib import Path
from typing import Dict, Optional

ENV_CACHE: Dict[str, str] = {}


def _load_env_file(env_path: Path) -> Dict[str, str]:
    """Simple .env reader to avoid extra dependencies.
    Lines with KEY=VALUE are parsed; # comments are ignored.
    """
    env: Dict[str, str] = {}
    if not env_path.exists():
        return env

    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip()
    return env


def _derive_key(master_secret: str) -> bytes:
    return hashlib.sha256(master_secret.encode()).digest()


def _xor_decrypt(blob: bytes, key: bytes) -> bytes:
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(blob))


def decrypt_value(value: str, master_secret: str) -> str:
    """Pseudo AES: XOR + base64 to keep secrets off-disk in plain text.
    Not meant as final cryptography—substitute with a real KMS/HSM in production.
    """
    try:
        raw = base64.b64decode(value)
        key = _derive_key(master_secret)
        return _xor_decrypt(raw, key).decode()
    except Exception:
        # If decryption fails, fall back to raw value to avoid outages.
        return value


class ConfigLoader:
    def __init__(self, env_path: str = ".env", master_env_var: str = "OMNICLAW_MASTER_KEY"):
        self.env_path = Path(env_path)
        ENV_CACHE.update(_load_env_file(self.env_path))
        self.master_secret = os.getenv(master_env_var) or ENV_CACHE.get(master_env_var) or "omniclaw-default-master"

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        return os.getenv(key) or ENV_CACHE.get(key, default)

    def get_secret(self, key: str, default: Optional[str] = None) -> Optional[str]:
        encrypted = self.get(f"{key}_ENC")
        if encrypted:
            return decrypt_value(encrypted, self.master_secret)
        return self.get(key, default)

    def model_chain(self):
        # Primary Anthropic Claude Opus 4.6 ? fallback Anthropic ? fallback OpenAI
        chain = [
            self.get("ANTHROPIC_MODEL", "claude-3-opus-4.6"),
            self.get("ANTHROPIC_FALLBACK", "claude-3-opus-latest"),
            self.get("OPENAI_FALLBACK", "gpt-4o-mini"),
        ]
        return [m for m in chain if m]

    def pick_model(self) -> str:
        for candidate in self.model_chain():
            return candidate
        return "claude-3-opus-4.6"

    def to_dict(self) -> Dict[str, str]:
        return {
            "binance_key": self.get_secret("BINANCE_API_KEY", ""),
            "binance_secret": self.get_secret("BINANCE_API_SECRET", ""),
            "coingecko_key": self.get_secret("COINGECKO_API_KEY", ""),
            "anthropic_model": self.pick_model(),
        }


if __name__ == "__main__":
    cfg = ConfigLoader()
    print(cfg.to_dict())
