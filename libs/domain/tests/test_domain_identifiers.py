from typing import Any
from uuid import UUID, uuid4

import mnemograph_domain
from mnemograph_domain import identifiers as domain_identifiers

APPROVED_IDENTIFIER_NAMES = {
    "ActorId",
    "GoalId",
    "GoalPlanId",
    "SubgoalId",
    "DeliberationSessionId",
    "DeliberationTurnId",
    "UserCheckpointId",
    "InterventionId",
}

DEFERRED_IDENTIFIER_NAMES = {
    "TransitionEventId",
    "ClaimId",
    "EvidenceLinkId",
    "EvidencePassageId",
    "ArchitectureIssueId",
}


def _identifier_map() -> dict[str, Any]:
    return {name: getattr(domain_identifiers, name) for name in APPROVED_IDENTIFIER_NAMES}


def _uuid_newtype_name_set() -> set[str]:
    names: set[str] = set()

    for name, value in vars(domain_identifiers).items():
        if getattr(value, "__supertype__", None) is UUID:
            names.add(name)

    return names


def test_identifiers_module_exposes_exact_eight_approved_identifier_newtypes() -> None:
    exported_identifier_names = _uuid_newtype_name_set()

    assert exported_identifier_names == APPROVED_IDENTIFIER_NAMES


def test_identifier_newtypes_have_uuid_supertype_and_stable_names() -> None:
    identifiers = _identifier_map()

    for name, identifier_type in identifiers.items():
        assert identifier_type.__supertype__ is UUID
        assert identifier_type.__name__ == name


def test_identifier_newtypes_are_all_distinct_objects() -> None:
    identifiers = _identifier_map()
    identifier_ids = {id(identifier_type) for identifier_type in identifiers.values()}

    assert len(identifier_ids) == len(APPROVED_IDENTIFIER_NAMES)


def test_identifier_newtypes_preserve_runtime_uuid_values() -> None:
    identifiers = _identifier_map()
    value = uuid4()

    for identifier_type in identifiers.values():
        assert identifier_type(value) == value


def test_deferred_identifier_names_are_absent_from_module_and_package_exports() -> None:
    package_exports = set(mnemograph_domain.__all__)

    for name in DEFERRED_IDENTIFIER_NAMES:
        assert not hasattr(domain_identifiers, name)
        assert name not in package_exports
