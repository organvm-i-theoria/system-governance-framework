"""Validation engine that runs governance rules against repository states."""

from __future__ import annotations

from dataclasses import dataclass, field

from .rules import BUILTIN_RULES, Rule


@dataclass
class ValidationResult:
    """Result of running a single rule."""

    rule_name: str
    passed: bool
    message: str
    severity: str = "error"


@dataclass
class ValidationReport:
    """Aggregate report from running all rules."""

    results: list[ValidationResult] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(r.passed for r in self.results if r.severity == "error")

    @property
    def error_count(self) -> int:
        return sum(1 for r in self.results if not r.passed and r.severity == "error")

    @property
    def warning_count(self) -> int:
        return sum(1 for r in self.results if not r.passed and r.severity == "warning")

    def summary(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        return (
            f"[{status}] {len(self.results)} rules checked, "
            f"{self.error_count} errors, {self.warning_count} warnings"
        )


class GovernanceValidator:
    """Runs governance rules against repository or organ state."""

    def __init__(self, rules: list[Rule] | None = None):
        self.rules = rules or BUILTIN_RULES

    def validate(self, state: dict) -> ValidationReport:
        report = ValidationReport()
        for rule in self.rules:
            passed, message = rule.check(state)
            report.results.append(
                ValidationResult(
                    rule_name=rule.name,
                    passed=passed,
                    message=message,
                    severity=rule.severity,
                )
            )
        return report

    def validate_many(self, states: list[dict]) -> list[ValidationReport]:
        return [self.validate(state) for state in states]
