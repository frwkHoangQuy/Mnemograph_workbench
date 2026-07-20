from mnemograph_domain import (
    ActorNotPermittedError,
    GoalVersionConflictError,
    IllegalGoalTransitionError,
    InvalidStructuralInputError,
)


def test_public_error_taxonomy_is_four_direct_value_error_subclasses() -> None:
    errors = {
        GoalVersionConflictError,
        IllegalGoalTransitionError,
        ActorNotPermittedError,
        InvalidStructuralInputError,
    }

    assert len(errors) == 4
    assert all(error.__bases__ == (ValueError,) for error in errors)
