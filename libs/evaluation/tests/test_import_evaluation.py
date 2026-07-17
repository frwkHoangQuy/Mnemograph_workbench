from importlib.metadata import version
from pathlib import Path


def test_import_evaluation() -> None:
    import evaluation

    assert version("mnemograph-evaluation") == "0.0.0"
    assert evaluation.__file__ is not None
    assert Path(evaluation.__file__).parts[-3:] == ("src", "evaluation", "__init__.py")
