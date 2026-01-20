## 2024-05-22 - [CLI Help Command Pattern]
**Learning:** Positional arguments in Bash scripts can easily swallow help flags (e.g., interpreting `-h` as a version string) if not intercepted early. This creates a confusing experience where users unintentionally trigger the script with invalid arguments instead of seeing instructions.
**Action:** Always intercept `-h` and `--help` flags *before* processing defaults or other arguments in CLI scripts to ensure help is always accessible.
