"""Shared path resolution for the selectively-extracted Görlitz rank data.

The full Görlitz ZIP set is ~76 GB; only ~33 specific rank folders are
needed (see scripts/extract_goerlitz_ranks.py), extracted into a single
GOERLITZ_EXTRACT_ROOT directory shared by hauptwerk_division.py,
oberwerk_division.py and pedal_division.py.

That directory is NOT committed (it's regenerable, large binary sample
data) and lives outside the repo by default - override its location with
the GOERLITZ_EXTRACT_ROOT environment variable (e.g. in CI, or once the
default scratch path has been cleaned up) rather than editing source.
"""
import os
import sys
from pathlib import Path

from src.codm.local_paths import installed_packages_root

_MAC_DEFAULT_EXTRACT_ROOT = Path(
    "/private/tmp/claude-501/-Users-pilepale-Documents-3D-metal-printing/"
    "fc14fe8b-9442-46d1-bef9-2a24ff20ea02/scratchpad/goerlitz-extract"
)

# Which ZIP part ("Sonus paradisi Goerlitz Sonnenorgel Hauptwerk (Part N).zip")
# each installation package's data lives in.
GOERLITZ_PART_FOR_PACKAGE = {1811: 1, 1812: 2, 1813: 3, 1814: 4}


def default_goerlitz_extract_root() -> Path:
    """GOERLITZ_EXTRACT_ROOT env var if set; else the scratch extraction on
    macOS, or Hauptwerk's installed OrganInstallationPackages elsewhere
    (Windows has Görlitz 001811-001814 installed directly in Hauptwerk)."""
    override = os.environ.get("GOERLITZ_EXTRACT_ROOT")
    if override:
        return Path(override)
    if sys.platform == "darwin":
        return _MAC_DEFAULT_EXTRACT_ROOT
    return installed_packages_root()


def goerlitz_package_root(extract_root: Path, package_id: int) -> Path:
    """Resolve an installation package's root dir within the extraction.

    Görlitz's own ZIPs are inconsistent about nesting: Part 1's package
    sits under HauptwerkSampleSetsAndComponents/OrganInstallationPackages/,
    while Parts 2-4 have their package directly at the ZIP root. Try both.
    extract_root may also be an installed OrganInstallationPackages folder,
    holding the package directly.
    """
    installed = extract_root / f"{package_id:06d}"
    if installed.is_dir():
        return installed
    part = GOERLITZ_PART_FOR_PACKAGE[package_id]
    base = extract_root / f"Sonus paradisi Goerlitz Sonnenorgel Hauptwerk (Part {part})"
    nested = base / "HauptwerkSampleSetsAndComponents" / "OrganInstallationPackages" / f"{package_id:06d}"
    flat = base / f"{package_id:06d}"
    return nested if nested.is_dir() else flat
