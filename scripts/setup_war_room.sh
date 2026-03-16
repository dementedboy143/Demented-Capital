#!/usr/bin/env bash
# Demented-Omni-Claw War Room Bootstrapper
# - Verifies signed skill bundle via SHA-256
# - Blocks known OpenClaw RCE vector CVE-2026-25253
# - Preps local venv and environment hygiene

set -euo pipefail

MIN_SAFE_GATEWAY_VERSION="1.6.2"  # versions below are considered vulnerable to CVE-2026-25253
SKILL_BUNDLE_PATH="${SKILL_BUNDLE_PATH:-./dist/demented_omni_claw.skill}"
SKILL_BUNDLE_SHA256="${SKILL_BUNDLE_SHA256:-}"  # optional env; otherwise read .sha256 file
VENV_DIR="${VENV_DIR:-.venv}"
REQUIREMENTS_FILE="${REQUIREMENTS_FILE:-requirements.txt}"
ENV_FILE="${ENV_FILE:-.env}"

red()   { printf "\033[31m%s\033[0m\n" "$1"; }
green() { printf "\033[32m%s\033[0m\n" "$1"; }
yellow(){ printf "\033[33m%s\033[0m\n" "$1"; }

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || { red "[FATAL] Missing required command: $1"; exit 1; }
}

version_lt() {
  # returns 0 if $1 < $2
  [ "$(printf '%s\n%s' "$1" "$2" | sort -V | head -n1)" != "$2" ]
}

check_cve_patch() {
  local gateway_version="${OPENCLAW_GATEWAY_VERSION:-}"
  if [[ -z "$gateway_version" && -f "/usr/local/openclaw/VERSION" ]]; then
    gateway_version=$(cat /usr/local/openclaw/VERSION)
  fi

  if [[ -z "$gateway_version" ]]; then
    yellow "[WARN] Unable to detect OpenClaw gateway version. Assuming hardened mode only."
    return 0
  fi

  if version_lt "$gateway_version" "$MIN_SAFE_GATEWAY_VERSION"; then
    red "[BLOCK] Gateway version $gateway_version < $MIN_SAFE_GATEWAY_VERSION (CVE-2026-25253 vulnerable). Patch before continuing."
    exit 1
  fi
  green "[OK] Gateway version $gateway_version is at or above patched level ($MIN_SAFE_GATEWAY_VERSION)."
}

verify_bundle() {
  require_cmd sha256sum
  if [[ ! -f "$SKILL_BUNDLE_PATH" ]]; then
    red "[FATAL] Skill bundle not found at $SKILL_BUNDLE_PATH"
    exit 1
  fi

  local expected
  if [[ -n "$SKILL_BUNDLE_SHA256" ]]; then
    expected="$SKILL_BUNDLE_SHA256"
  elif [[ -f "${SKILL_BUNDLE_PATH}.sha256" ]]; then
    expected=$(cut -d ' ' -f1 "${SKILL_BUNDLE_PATH}.sha256")
  else
    red "[FATAL] No expected SHA-256 provided. Set SKILL_BUNDLE_SHA256 or add ${SKILL_BUNDLE_PATH}.sha256"
    exit 1
  fi

  local computed
  computed=$(sha256sum "$SKILL_BUNDLE_PATH" | awk '{print $1}')
  printf "Expected SHA-256 : %s\nComputed SHA-256 : %s\n" "$expected" "$computed"
  if [[ "$expected" != "$computed" ]]; then
    red "[BLOCK] Bundle integrity FAILED. Aborting load."
    exit 1
  fi
  green "[OK] Bundle integrity verified."
}

secure_env_file() {
  if [[ -f "$ENV_FILE" ]]; then
    chmod 600 "$ENV_FILE" || true
    green "[OK] Locked permissions on $ENV_FILE"
  else
    yellow "[WARN] $ENV_FILE not found; skipping permission hardening"
  fi
}

create_venv() {
  require_cmd python3
  if [[ ! -d "$VENV_DIR" ]]; then
    python3 -m venv "$VENV_DIR"
    green "[OK] Virtualenv created at $VENV_DIR"
  fi
  # shellcheck disable=SC1090
  source "$VENV_DIR/bin/activate"
  if [[ -f "$REQUIREMENTS_FILE" ]]; then
    pip install --upgrade pip >/dev/null
    pip install -r "$REQUIREMENTS_FILE"
    green "[OK] Dependencies installed from $REQUIREMENTS_FILE"
  else
    yellow "[WARN] $REQUIREMENTS_FILE not found; skipping dependency install"
  fi
}

main() {
  check_cve_patch
  verify_bundle
  secure_env_file
  create_venv
  green "[DONE] War Room bootstrap complete. Ready to run manual_strike --demo or daemon modes."
}

main "$@"
