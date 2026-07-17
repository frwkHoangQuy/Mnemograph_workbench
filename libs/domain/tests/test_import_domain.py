from importlib.metadata import version
from pathlib import Path


def test_import_domain() -> None:
    import mnemograph_domain

    assert version("mnemograph-domain") == "0.0.0"
    assert mnemograph_domain.__file__ is not None
    assert Path(mnemograph_domain.__file__).parts[-3:] == (
        "src",
        "mnemograph_domain",
        "__init__.py",
    )
    assert not (Path(__file__).parents[1] / "src" / "domain").exists()
