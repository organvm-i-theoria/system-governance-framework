"""Configuration loader for the System Governance Framework.

Reads governance.yml files, resolves preset defaults, and merges
user overrides to produce a fully-resolved configuration dict.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

PRESETS_DIR = Path(__file__).resolve().parent.parent / "config" / "presets"
SCHEMA_PATH = Path(__file__).resolve().parent.parent / "config" / "schema.json"

VALID_PRESETS = ("minimal", "standard", "enterprise")


class ConfigError(Exception):
    """Raised when a governance configuration is invalid."""


def load_preset(name: str) -> dict[str, Any]:
    """Load a preset YAML file by name and return it as a dict."""
    if name not in VALID_PRESETS:
        raise ConfigError(
            f"Unknown preset '{name}'. Valid presets: {', '.join(VALID_PRESETS)}"
        )
    preset_path = PRESETS_DIR / f"{name}.yml"
    if not preset_path.exists():
        raise ConfigError(f"Preset file not found: {preset_path}")
    with open(preset_path) as f:
        return yaml.safe_load(f)


def load_schema() -> dict[str, Any]:
    """Load the JSON Schema for governance.yml validation."""
    if not SCHEMA_PATH.exists():
        raise ConfigError(f"Schema file not found: {SCHEMA_PATH}")
    with open(SCHEMA_PATH) as f:
        return json.load(f)


def _deep_merge(base: dict, override: dict) -> dict:
    """Recursively merge override into base, returning a new dict.

    Override values take precedence. Nested dicts are merged recursively;
    all other types are replaced outright.
    """
    merged = dict(base)
    for key, value in override.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_governance_config(path: str | Path) -> dict[str, Any]:
    """Load a governance.yml file with preset resolution.

    Steps:
      1. Read the user's governance.yml
      2. Determine the preset (defaults to 'standard')
      3. Load preset defaults
      4. Deep-merge user overrides on top of preset defaults
      5. Return the fully-resolved config dict
    """
    path = Path(path)
    if not path.exists():
        raise ConfigError(f"Configuration file not found: {path}")

    with open(path) as f:
        user_config = yaml.safe_load(f)

    if not isinstance(user_config, dict):
        raise ConfigError("Configuration file must contain a YAML mapping")

    # Extract framework section
    framework = user_config.get("framework", {})
    if not isinstance(framework, dict):
        raise ConfigError("'framework' must be a mapping")

    if "version" not in framework:
        raise ConfigError("'framework.version' is required")

    # Resolve preset
    preset_name = framework.get("preset", "standard")
    preset_config = load_preset(preset_name)

    # Merge: preset defaults as base, user config as override
    resolved = _deep_merge(preset_config, user_config)

    return resolved


def config_to_repo_state(config: dict[str, Any]) -> dict[str, Any]:
    """Convert a resolved governance config into a repo-state dict
    suitable for passing to the GovernanceValidator.

    This bridges the config system with the rules engine.
    """
    features = config.get("features", {})
    ci = features.get("ci", {})
    security = features.get("security", {})
    quality = features.get("quality", {})
    compliance = features.get("compliance", {})

    preset = config.get("framework", {}).get("preset", "standard")

    return {
        "preset": preset,
        "ci_enabled": ci.get("enabled", True),
        "test_coverage_enabled": ci.get("test-coverage", False),
        "security_enabled": security.get("enabled", True),
        "codeql_enabled": security.get("codeql", False),
        "semgrep_enabled": security.get("semgrep", False),
        "dependency_scan_enabled": security.get("dependency-scan", True),
        "quality_enabled": quality.get("enabled", True),
        "linting_enabled": quality.get("linting", True),
        "pre_commit_enabled": quality.get("pre-commit", False),
        "compliance_enabled": compliance.get("enabled", False),
    }
