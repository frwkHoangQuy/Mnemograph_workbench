from uuid import UUID

import pytest
from mnemograph_contracts.enums import GoalState
from mnemograph_contracts.goals import GoalCreateRequest, GoalResponse
from pydantic import ValidationError


def test_goal_create_request_valid() -> None:
    request = GoalCreateRequest(statement="Improve evidence quality")
    assert request.statement == "Improve evidence quality"


def test_goal_response_valid_and_optional_default() -> None:
    response = GoalResponse(
        goal_id=UUID("00000000-0000-0000-0000-000000000001"),
        statement="Improve evidence quality",
        state=GoalState.DRAFT,
        version=0,
    )
    assert response.approved_goal_plan_id is None


def test_goal_response_valid_json_uuid() -> None:
    response = GoalResponse.model_validate_json(
        '{"goal_id":"00000000-0000-0000-0000-000000000001","statement":"x","state":"DRAFT","version":0}'
    )
    assert response.goal_id == UUID("00000000-0000-0000-0000-000000000001")


def test_goal_create_request_empty_statement_fails() -> None:
    with pytest.raises(ValidationError):
        GoalCreateRequest(statement="")


def test_goal_response_invalid_state_fails() -> None:
    with pytest.raises(ValidationError):
        GoalResponse.model_validate_json(
            '{"goal_id":"00000000-0000-0000-0000-000000000001","statement":"x","state":"ACCEPTED","version":0}'
        )


def test_goal_response_negative_version_fails() -> None:
    with pytest.raises(ValidationError):
        GoalResponse(
            goal_id=UUID("00000000-0000-0000-0000-000000000001"),
            statement="x",
            state=GoalState.DRAFT,
            version=-1,
        )


def test_goal_response_unknown_field_fails() -> None:
    with pytest.raises(ValidationError):
        GoalResponse.model_validate_json(
            '{"goal_id":"00000000-0000-0000-0000-000000000001","statement":"x","state":"DRAFT","version":0,"extra":1}'
        )


def test_goal_response_frozen_assignment_fails() -> None:
    response = GoalResponse(
        goal_id=UUID("00000000-0000-0000-0000-000000000001"),
        statement="x",
        state=GoalState.DRAFT,
        version=0,
    )
    with pytest.raises(ValidationError):
        response.statement = "y"
