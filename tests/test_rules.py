"""Tests for governance rules."""

from src.rules import (
    BUILTIN_RULES,
    check_documentation_status,
    check_implementation_status,
    check_license_exists,
    check_no_back_edges,
    check_readme_exists,
)


class TestReadmeRule:
    def test_passes_when_readme_exists(self):
        passed, msg = check_readme_exists({"has_readme": True})
        assert passed is True

    def test_fails_when_readme_missing(self):
        passed, msg = check_readme_exists({"has_readme": False})
        assert passed is False

    def test_fails_when_key_absent(self):
        passed, msg = check_readme_exists({})
        assert passed is False


class TestLicenseRule:
    def test_passes_when_license_exists(self):
        passed, msg = check_license_exists({"has_license": True})
        assert passed is True

    def test_fails_when_license_missing(self):
        passed, msg = check_license_exists({})
        assert passed is False


class TestNoBackEdges:
    def test_no_dependencies(self):
        passed, msg = check_no_back_edges({"organ": "I", "dependencies": []})
        assert passed is True

    def test_valid_forward_dependency(self):
        state = {"organ": "I", "dependencies": [{"organ": "I"}]}
        passed, msg = check_no_back_edges(state)
        assert passed is True

    def test_detects_back_edge(self):
        state = {"organ": "III", "dependencies": [{"organ": "IV"}]}
        passed, msg = check_no_back_edges(state)
        assert passed is False
        assert "Back-edge" in msg

    def test_allows_same_organ_dependency(self):
        state = {"organ": "II", "dependencies": [{"organ": "II"}]}
        passed, msg = check_no_back_edges(state)
        assert passed is True


class TestDocumentationStatus:
    def test_valid_deployed(self):
        passed, _ = check_documentation_status({"documentation_status": "DEPLOYED"})
        assert passed is True

    def test_valid_skeleton(self):
        passed, _ = check_documentation_status({"documentation_status": "SKELETON"})
        assert passed is True

    def test_invalid_status(self):
        passed, msg = check_documentation_status({"documentation_status": "BROKEN"})
        assert passed is False


class TestImplementationStatus:
    def test_valid_production(self):
        passed, _ = check_implementation_status({"implementation_status": "PRODUCTION"})
        assert passed is True

    def test_invalid_status(self):
        passed, _ = check_implementation_status({"implementation_status": "UNKNOWN"})
        assert passed is False


class TestBuiltinRules:
    def test_all_rules_registered(self):
        assert len(BUILTIN_RULES) >= 5

    def test_all_rules_have_names(self):
        for rule in BUILTIN_RULES:
            assert rule.name
            assert rule.description
