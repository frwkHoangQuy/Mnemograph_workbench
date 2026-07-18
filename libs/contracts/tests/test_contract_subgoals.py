from uuid import UUID

import pytest
from mnemograph_contracts.enums import SubgoalAcceptanceStatus
from mnemograph_contracts.subgoals import SubgoalCreateRequest, SubgoalResponse
from pydantic import ValidationError


def test_subgoal_create_request_valid() -> None:
    request = SubgoalCreateRequest(
        goal_id=UUID("00000000-0000-0000-0000-000000000001"),
        statement="Propose criteria",
        definition_of_done="Criteria accepted",
    )
    assert request.statement == "Propose criteria"


def test_subgoal_response_valid_for_both_statuses() -> None:
    for status in (SubgoalAcceptanceStatus.NOT_ACCEPTED, SubgoalAcceptanceStatus.USER_ACCEPTED):
        response = SubgoalResponse(
            subgoal_id=UUID("00000000-0000-0000-0000-000000000010"),
            goal_id=UUID("00000000-0000-0000-0000-000000000001"),
            statement="Propose criteria",
            definition_of_done="Criteria accepted",
            version=0,
            acceptance_status=status,
        )
        assert response.acceptance_status is status


def test_subgoal_create_request_empty_statement_fails() -> None:
    with pytest.raises(ValidationError):
        SubgoalCreateRequest(
            goal_id=UUID("00000000-0000-0000-0000-000000000001"),
            statement="",
            definition_of_done="ok",
        )


def test_subgoal_create_request_empty_definition_of_done_fails() -> None:
    with pytest.raises(ValidationError):
        SubgoalCreateRequest(
            goal_id=UUID("00000000-0000-0000-0000-000000000001"),
            statement="x",
            definition_of_done="",
        )


def test_subgoal_response_invalid_status_token_fails() -> None:
    with pytest.raises(ValidationError):
        SubgoalResponse.model_validate_json(
            '{"subgoal_id":"00000000-0000-0000-0000-000000000010","goal_id":"00000000-0000-0000-0000-000000000001","statement":"x","definition_of_done":"d","version":0,"acceptance_status":"ACCEPTED"}'
        )


def test_subgoal_response_negative_version_fails() -> None:
    with pytest.raises(ValidationError):
        SubgoalResponse(
            subgoal_id=UUID("00000000-0000-0000-0000-000000000010"),
            goal_id=UUID("00000000-0000-0000-0000-000000000001"),
            statement="x",
            definition_of_done="d",
            version=-1,
            acceptance_status=SubgoalAcceptanceStatus.NOT_ACCEPTED,
        )


def test_subgoal_response_unknown_field_fails() -> None:
    with pytest.raises(ValidationError):
        SubgoalResponse.model_validate_json(
            '{"subgoal_id":"00000000-0000-0000-0000-000000000010","goal_id":"00000000-0000-0000-0000-000000000001","statement":"x","definition_of_done":"d","version":0,"acceptance_status":"NOT_ACCEPTED","extra":1}'
        )


def test_subgoal_response_frozen_assignment_fails() -> None:
    response = SubgoalResponse(
        subgoal_id=UUID("00000000-0000-0000-0000-000000000010"),
        goal_id=UUID("00000000-0000-0000-0000-000000000001"),
        statement="x",
        definition_of_done="d",
        version=0,
        acceptance_status=SubgoalAcceptanceStatus.NOT_ACCEPTED,
    )
    with pytest.raises(ValidationError):
        response.statement = "y"
