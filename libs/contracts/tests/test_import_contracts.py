from importlib.metadata import version
from pathlib import Path


def test_import_contracts() -> None:
    import contracts

    assert version("mnemograph-contracts") == "0.0.0"
    assert contracts.__file__ is not None
    assert Path(contracts.__file__).parts[-3:] == ("src", "contracts", "__init__.py")
