"""Machine-specific locations of Hauptwerk data and the source sample sets.

The project is developed on two machines:

* macOS - the source sample sets live on an external drive
  (/Volumes/Samsung T7/Orgulje/...), Görlitz as a selective ZIP extraction.
* Windows - every package is installed in Hauptwerk itself under
  ~/Hauptwerk/HauptwerkSampleSetsAndComponents/OrganInstallationPackages.

Defaults pick whichever layout is present; override with environment
variables rather than editing source:

* HAUPTWERK_ROOT      - the Hauptwerk data folder (default: ~/Hauptwerk)
* SAMPLE_SETS_ROOT    - folder holding the "<Organ>/OrganInstallationPackages"
                        trees (default: /Volumes/Samsung T7/Orgulje on macOS)
* GOERLITZ_EXTRACT_ROOT - see goerlitz_paths.py
"""
import os
import sys
from pathlib import Path

_MAC_SAMPLE_SETS_ROOT = Path("/Volumes/Samsung T7/Orgulje")

WALTERSHAUSEN_PACKAGE_ID = 255
WASSELONNE_PACKAGE_ID = 802
ZOBLITZ_PACKAGE_ID = 458


def hauptwerk_root() -> Path:
    override = os.environ.get("HAUPTWERK_ROOT")
    return Path(override) if override else Path.home() / "Hauptwerk"


def custom_organ_definitions_dir() -> Path:
    return hauptwerk_root() / "HauptwerkUserData" / "CustomOrganDefinitions"


def installed_packages_root() -> Path:
    """Hauptwerk's own OrganInstallationPackages folder."""
    return hauptwerk_root() / "HauptwerkSampleSetsAndComponents" / "OrganInstallationPackages"


def _sample_sets_root() -> Path | None:
    """External sample-set drive, or None to use Hauptwerk's installed packages."""
    override = os.environ.get("SAMPLE_SETS_ROOT")
    if override:
        return Path(override)
    if sys.platform == "darwin":
        return _MAC_SAMPLE_SETS_ROOT
    return None


def _packages_root(organ_folder: str) -> Path:
    ext = _sample_sets_root()
    if ext is None:
        return installed_packages_root()
    return ext / organ_folder / "OrganInstallationPackages"


def waltershausen_root() -> Path:
    """Folder that CONTAINS package 000255 (callers append the package id)."""
    return _packages_root("Trost Waltershausen")


def wasselonne_root() -> Path:
    return _packages_root("Silbermann Wasselonne") / f"{WASSELONNE_PACKAGE_ID:06d}"


def zoblitz_root() -> Path:
    return _packages_root("Stadtkirche Zoeblitz") / f"{ZOBLITZ_PACKAGE_ID:06d}"
