import ast
import sys
from pathlib import Path

import mnemograph_domain

APPROVED_EXPORTS = {
    "ActorId",
    "GoalId",
    "GoalPlanId",
    "SubgoalId",
    "DeliberationSessionId",
    "DeliberationTurnId",
    "UserCheckpointId",
    "InterventionId",
    "ActorKind",
    "GoalState",
    "SubgoalAcceptanceStatus",
    "DeliberationSessionState",
    "InterventionKind",
    "AggregateVersion",
    "make_aggregate_version",
    "ActorRef",
}

FORBIDDEN_EXPORTS = {
    "TransitionEventId",
    "ClaimId",
    "EvidenceLinkId",
    "EvidencePassageId",
    "ArchitectureIssueId",
    "EvidenceRelationship",
    "UtcDateTime",
    "ACCEPTED",
    "PUBLISHING",
    "COMPLETED",
}


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _module_name_from_file(package_root: Path, file_path: Path) -> str:
    relative_parts = file_path.relative_to(package_root).with_suffix("").parts
    return ".".join(("mnemograph_domain", *relative_parts))


def _import_roots(module_source: str) -> list[str]:
    roots: list[str] = []
    parsed = ast.parse(module_source)

    for node in ast.walk(parsed):
        if isinstance(node, ast.Import):
            for alias in node.names:
                roots.append(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.level > 0:
                roots.append("mnemograph_domain")
            elif node.module is not None:
                roots.append(node.module.split(".")[0])

    return roots


def test_domain_python_files_import_only_stdlib_or_domain_modules() -> None:
    package_root = _repo_root() / "libs" / "domain" / "src" / "mnemograph_domain"
    python_files = sorted(package_root.rglob("*.py"))

    assert python_files

    for module_file in python_files:
        module_source = module_file.read_text(encoding="utf-8")
        module_name = _module_name_from_file(package_root, module_file)
        for import_root in _import_roots(module_source):
            assert import_root == "mnemograph_domain" or import_root in sys.stdlib_module_names, (
                f"{module_name} imports disallowed dependency root {import_root}"
            )


def test_contracts_production_files_do_not_import_domain_package() -> None:
    contracts_root = _repo_root() / "libs" / "contracts" / "src" / "mnemograph_contracts"
    contract_files = sorted(contracts_root.rglob("*.py"))

    assert contract_files

    for contract_file in contract_files:
        source = contract_file.read_text(encoding="utf-8")
        roots = _import_roots(source)
        assert "mnemograph_domain" not in roots


def test_domain_public_export_surface_is_exact_and_has_no_duplicates() -> None:
    exports = list(mnemograph_domain.__all__)

    assert len(exports) == len(set(exports))
    assert set(exports) == APPROVED_EXPORTS


def test_domain_package_does_not_define_module_level_version() -> None:
    assert not hasattr(mnemograph_domain, "__version__")


def test_forbidden_and_deferred_symbols_are_not_exported() -> None:
    exports = set(mnemograph_domain.__all__)

    for symbol_name in FORBIDDEN_EXPORTS:
        assert symbol_name not in exports


def test_domain_production_package_has_no_datetime_imports_or_datetime_public_helpers() -> None:
    package_root = _repo_root() / "libs" / "domain" / "src" / "mnemograph_domain"
    python_files = sorted(package_root.rglob("*.py"))
    exports = set(mnemograph_domain.__all__)

    for module_file in python_files:
        source = module_file.read_text(encoding="utf-8")
        assert "datetime" not in _import_roots(source)

    assert all("datetime" not in symbol_name.lower() for symbol_name in exports)


def test_domain_public_exports_have_no_custom_exception_surface() -> None:
    exported_objects = [
        getattr(mnemograph_domain, symbol_name) for symbol_name in mnemograph_domain.__all__
    ]
    exported_exception_classes = {
        exported_object
        for exported_object in exported_objects
        if isinstance(exported_object, type) and issubclass(exported_object, BaseException)
    }

    assert not exported_exception_classes
