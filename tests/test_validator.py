"""Tests for the governance validator."""

from src.rules import Rule
from src.validator import GovernanceValidator, ValidationReport


class TestValidationReport:
    def test_empty_report_passes(self):
        report = ValidationReport()
        assert report.passed is True
        assert report.error_count == 0

    def test_all_pass(self):
        validator = GovernanceValidator()
        state = {
            "has_readme": True,
            "has_license": True,
            "organ": "I",
            "dependencies": [],
            "documentation_status": "DEPLOYED",
            "implementation_status": "PRODUCTION",
        }
        report = validator.validate(state)
        assert report.passed is True
        assert report.error_count == 0

    def test_failing_rule(self):
        validator = GovernanceValidator()
        state = {"has_readme": False, "has_license": False}
        report = validator.validate(state)
        assert report.passed is False
        assert report.error_count >= 2

    def test_summary_format(self):
        report = ValidationReport()
        summary = report.summary()
        assert "PASS" in summary or "FAIL" in summary


class TestValidateMany:
    def test_validates_multiple_states(self):
        validator = GovernanceValidator()
        states = [
            {"has_readme": True, "has_license": True, "documentation_status": "DEPLOYED",
             "implementation_status": "PRODUCTION", "organ": "I", "dependencies": []},
            {"has_readme": False},
        ]
        reports = validator.validate_many(states)
        assert len(reports) == 2
        assert reports[0].passed is True
        assert reports[1].passed is False


class TestCustomRules:
    def test_custom_rule(self):
        custom = Rule(
            name="custom-test",
            description="Always passes",
            check=lambda s: (True, "OK"),
        )
        validator = GovernanceValidator(rules=[custom])
        report = validator.validate({})
        assert report.passed is True
        assert len(report.results) == 1
