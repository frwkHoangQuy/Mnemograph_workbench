class GoalVersionConflictError(ValueError):
    pass


class IllegalGoalTransitionError(ValueError):
    pass


class ActorNotPermittedError(ValueError):
    pass


class InvalidStructuralInputError(ValueError):
    pass
