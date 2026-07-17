from importlib.metadata import version
from pathlib import Path


def test_import_contracts() -> None:
    import mnemograph_contracts

    assert version("mnemograph-contracts") == "0.0.0"
    assert mnemograph_contracts.__file__ is not None
    assert Path(mnemograph_contracts.__file__).parts[-3:] == (
        "src",
        "mnemograph_contracts",
        "__init__.py",
    )
    assert not (Path(__file__).parents[1] / "src" / "contracts").exists()
