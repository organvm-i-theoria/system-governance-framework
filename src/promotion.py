"""Promotion state machine for repository lifecycle.

States: PLANNED → SKELETON → PROTOTYPE → PRODUCTION → ARCHIVED
"""

from __future__ import annotations

from dataclasses import dataclass

VALID_TRANSITIONS: dict[str, set[str]] = {
    "PLANNED": {"SKELETON"},
    "SKELETON": {"PROTOTYPE", "DESIGN_ONLY"},
    "DESIGN_ONLY": {"PROTOTYPE", "SKELETON"},
    "PROTOTYPE": {"PRODUCTION", "SKELETON"},
    "PRODUCTION": {"ARCHIVED", "PROTOTYPE"},
    "ARCHIVED": {"PRODUCTION"},  # un-archive is allowed
}

ALL_STATES = set(VALID_TRANSITIONS.keys()) | {"ARCHIVED"}


@dataclass
class PromotionResult:
    """Result of a promotion attempt."""

    success: bool
    from_state: str
    to_state: str
    message: str


def can_promote(current: str, target: str) -> bool:
    """Check if a transition from current to target is valid."""
    allowed = VALID_TRANSITIONS.get(current, set())
    return target in allowed


def promote(current: str, target: str, repo_name: str = "") -> PromotionResult:
    """Attempt to promote a repo from current state to target state."""
    if current not in ALL_STATES:
        return PromotionResult(False, current, target, f"Unknown state: {current}")
    if target not in ALL_STATES:
        return PromotionResult(False, current, target, f"Unknown target state: {target}")
    if can_promote(current, target):
        return PromotionResult(
            True, current, target,
            f"{repo_name or 'Repo'}: {current} → {target}"
        )
    allowed = VALID_TRANSITIONS.get(current, set())
    return PromotionResult(
        False, current, target,
        f"Cannot promote from {current} to {target}. Allowed: {sorted(allowed)}"
    )
