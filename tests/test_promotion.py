"""Tests for the promotion state machine."""

from src.promotion import ALL_STATES, VALID_TRANSITIONS, can_promote, promote


class TestCanPromote:
    def test_planned_to_skeleton(self):
        assert can_promote("PLANNED", "SKELETON") is True

    def test_skeleton_to_prototype(self):
        assert can_promote("SKELETON", "PROTOTYPE") is True

    def test_prototype_to_production(self):
        assert can_promote("PROTOTYPE", "PRODUCTION") is True

    def test_production_to_archived(self):
        assert can_promote("PRODUCTION", "ARCHIVED") is True

    def test_cannot_skip_states(self):
        assert can_promote("PLANNED", "PRODUCTION") is False

    def test_cannot_go_backwards_planned(self):
        assert can_promote("PROTOTYPE", "PLANNED") is False

    def test_unarchive_allowed(self):
        assert can_promote("ARCHIVED", "PRODUCTION") is True

    def test_design_only_to_prototype(self):
        assert can_promote("DESIGN_ONLY", "PROTOTYPE") is True


class TestPromote:
    def test_successful_promotion(self):
        result = promote("SKELETON", "PROTOTYPE", "test-repo")
        assert result.success is True
        assert "SKELETON → PROTOTYPE" in result.message

    def test_failed_promotion(self):
        result = promote("PLANNED", "PRODUCTION", "test-repo")
        assert result.success is False
        assert "Cannot promote" in result.message

    def test_unknown_state(self):
        result = promote("INVALID", "SKELETON")
        assert result.success is False
        assert "Unknown state" in result.message

    def test_unknown_target(self):
        result = promote("SKELETON", "INVALID")
        assert result.success is False
        assert "Unknown target" in result.message


class TestStateMachine:
    def test_all_states_have_transitions(self):
        for state in VALID_TRANSITIONS:
            assert len(VALID_TRANSITIONS[state]) >= 1

    def test_no_self_transitions(self):
        for state, targets in VALID_TRANSITIONS.items():
            assert state not in targets

    def test_full_lifecycle(self):
        path = ["PLANNED", "SKELETON", "PROTOTYPE", "PRODUCTION", "ARCHIVED"]
        for i in range(len(path) - 1):
            assert can_promote(path[i], path[i + 1]), f"{path[i]} → {path[i+1]} should be valid"
