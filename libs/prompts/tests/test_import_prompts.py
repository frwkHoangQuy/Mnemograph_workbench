from importlib.metadata import version
from pathlib import Path


def test_import_prompts() -> None:
    import prompts

    assert version("mnemograph-prompts") == "0.0.0"
    assert prompts.__file__ is not None
    assert Path(prompts.__file__).parts[-3:] == ("src", "prompts", "__init__.py")
