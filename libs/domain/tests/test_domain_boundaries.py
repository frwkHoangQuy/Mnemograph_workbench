from pathlib import Path

FORBIDDEN_IMPORT_PREFIXES = (
    "pydantic",
    "fastapi",
    "sqlalchemy",
    "mnemograph_contracts",
)


def test_domain_source_does_not_import_forbidden_runtime_dependencies() -> None:
    src_root = Path(__file__).parents[1] / "src" / "mnemograph_domain"
    python_files = sorted(path for path in src_root.glob("*.py") if path.name != "__init__.py")

    assert python_files

    for module_file in python_files:
        module_text = module_file.read_text(encoding="utf-8")
        for forbidden_prefix in FORBIDDEN_IMPORT_PREFIXES:
            assert f"import {forbidden_prefix}" not in module_text
            assert f"from {forbidden_prefix}" not in module_text
