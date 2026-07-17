from importlib.metadata import version
from pathlib import Path


def test_import_domain() -> None:
    import domain

    assert version("mnemograph-domain") == "0.0.0"
    assert domain.__file__ is not None
    assert Path(domain.__file__).parts[-3:] == ("src", "domain", "__init__.py")
