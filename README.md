[![ORGAN-I: Theory](https://img.shields.io/badge/ORGAN--I-Theory-1a237e?style=flat-square)](https://github.com/organvm-i-theoria)

# System Governance Framework

**Canonical governance templates and enforcement infrastructure for the eight-organ creative-institutional system.**

## Purpose

Every repository across the eight ORGAN organisations needs a shared baseline of governance: security policies, code ownership rules, issue templates, contributor guidelines, and automated quality gates. This repository is that baseline. It provides the reference implementation of community-health files (`.github/` directory), pre-commit hooks, CI workflows, and Dependabot configuration that all ORGAN repos either adopt directly or adapt for their domain.

Within the ORGAN-I (Theoria) organ, this repo occupies a structural role rather than a theoretical one. Where other ORGAN-I repositories explore epistemology, recursion, and cognitive architecture, System Governance Framework operationalises those ideas into enforceable standards. It answers the question: *given a set of principles about how knowledge should be organised, what do the actual contribution guardrails look like?*

The framework ships with structured issue templates (bug reports, feature requests, questions), a pull-request template, a security advisory policy, CODEOWNERS configuration, and pre-commit hooks covering whitespace normalisation, secret detection, YAML/JSON/TOML validation, and merge-conflict prevention. Dependabot is configured for weekly GitHub Actions dependency updates. A multi-agent handoff protocol (under `.github/agents/`) coordinates AI-assisted documentation and review workflows that align with the project's AI-conductor model.

## What Is Included

| Directory | Contents |
|-----------|----------|
| `.github/ISSUE_TEMPLATE/` | Bug report, feature request, and question templates (YAML) |
| `.github/workflows/` | CI pipeline: pre-commit validation on push and PR |
| `.github/agents/` | Coordinator config, handoff protocols, task templates for AI agents |
| `.github/actions/` | Composite actions: language detection, config loading |
| `.github/SECURITY.md` | Vulnerability reporting and response policy |
| `.github/CODEOWNERS` | Code ownership rules |
| `.github/dependabot.yml` | Automated dependency update schedule |

## Status

**Stub / Governance Seed** -- The governance scaffolding is deployed and functional. Ongoing work involves propagating these standards to all 79 repositories across the eight ORGAN organisations and adapting templates for organ-specific needs (e.g., ORGAN-III commercial repos require additional licensing language; ORGAN-V public-process repos require editorial review gates).

## Relationship to the Eight-Organ System

This repository is one of 18 in [ORGAN-I: Theoria](https://github.com/organvm-i-theoria), the theoretical and epistemological foundation of the system. It sits at the infrastructure layer, providing governance primitives consumed by ORGAN-IV (Taxis / Orchestration) for cross-organ enforcement and by every individual organ for local compliance.

## Author

**[@4444J99](https://github.com/4444J99)** / Part of [ORGAN-I: Theoria](https://github.com/organvm-i-theoria)
