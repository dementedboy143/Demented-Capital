"""Generate a deterministic dummy skill bundle + SHA-256 for CI/contest verification."""
from __future__ import annotations

import gzip
import hashlib
import tarfile
from pathlib import Path

DIST_DIR = Path("dist")
BUNDLE_NAME = "omni_claw_skill.tar.gz"
BUNDLE_SHA = "omni_claw_skill.sha256"


def build_dummy_files(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    manifest = root / "manifest.txt"
    manifest.write_text("Demented-Omni-Claw skill bundle (demo)\n", encoding="utf-8")
    return manifest


def create_bundle() -> Path:
    DIST_DIR.mkdir(exist_ok=True)
    bundle_root = DIST_DIR / "omni_claw_skill"
    build_dummy_files(bundle_root)

    bundle_path = DIST_DIR / BUNDLE_NAME

    def _reset_info(ti: tarfile.TarInfo) -> tarfile.TarInfo:
        ti.uid = ti.gid = 0
        ti.uname = ti.gname = ""
        ti.mtime = 0
        if ti.isfile():
            ti.mode = 0o644
        else:
            ti.mode = 0o755
        return ti

    with bundle_path.open("wb") as f_out:
        with gzip.GzipFile(fileobj=f_out, mode="wb", mtime=0) as gz:
            with tarfile.open(fileobj=gz, mode="w") as tar:
                tar.add(str(bundle_root), arcname=bundle_root.name, filter=_reset_info)

    return bundle_path


def write_sha256(bundle_path: Path) -> Path:
    sha_path = bundle_path.with_suffix(".sha256")
    digest = hashlib.sha256(bundle_path.read_bytes()).hexdigest()
    sha_path.write_text(f"{digest}  {bundle_path.name}\n", encoding="utf-8")
    return sha_path


def main():
    bundle = create_bundle()
    sha_file = write_sha256(bundle)
    print(f"[OK] Bundle: {bundle}")
    print(f"[OK] SHA-256 written to: {sha_file}")


if __name__ == "__main__":
    main()
