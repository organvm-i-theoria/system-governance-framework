## 2026-01-20 - Script Argument Injection in Installer

**Vulnerability:** Found a Script Argument Injection vulnerability in `scripts/install-framework.sh` where unvalidated arguments (`VERSION`) could be used to inject malicious YAML into generated workflow files.
**Learning:** Shell scripts using user input to generate files via heredocs/cat are vulnerable to content injection if inputs are not strictly validated, even if they don't execute commands directly.
**Prevention:** Always validate shell script arguments against a strict allowlist (regex) before using them in any context, especially file generation or command construction.
