from importlib.metadata import version
from pathlib import Path


def test_import_model_gateway() -> None:
    import model_gateway

    assert version("mnemograph-model-gateway") == "0.0.0"
    assert model_gateway.__file__ is not None
    assert Path(model_gateway.__file__).parts[-3:] == ("src", "model_gateway", "__init__.py")
