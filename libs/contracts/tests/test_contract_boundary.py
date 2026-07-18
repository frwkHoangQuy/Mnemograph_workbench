from pathlib import Path


def test_contract_package_boundary_imports() -> None:
    import mnemograph_contracts

    assert mnemograph_contracts is not None


def test_no_disallowed_imports_in_contract_sources() -> None:
    src_dir = Path(__file__).parents[1] / "src" / "mnemograph_contracts"
    disallowed = [
        "mnemograph_domain",
        "fastapi",
        "sqlalchemy",
        "psycopg",
        "openai",
        "anthropic",
        "google.generativeai",
    ]

    for py_file in src_dir.glob("*.py"):
        content = py_file.read_text(encoding="utf-8")
        for token in disallowed:
            assert token not in content


def test_no_mutable_public_payload_fields() -> None:
    src_dir = Path(__file__).parents[1] / "src" / "mnemograph_contracts"
    content = "\n".join(file.read_text(encoding="utf-8") for file in src_dir.glob("*.py"))
    assert "payload:" not in content
    assert "dict[" not in content
    assert "list[" not in content
