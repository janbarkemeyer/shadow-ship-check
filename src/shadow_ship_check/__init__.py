"""Shadow Ship Check - camouflage indicators for ships near subsea cable incidents."""

__version__ = "0.2.0"


def data_path():
    """Bundled data in an installed wheel, or the editable checkout."""
    from pathlib import Path

    packaged = Path(__file__).resolve().parent / "_data"
    return packaged if packaged.is_dir() else Path(__file__).resolve().parents[2] / "data"
