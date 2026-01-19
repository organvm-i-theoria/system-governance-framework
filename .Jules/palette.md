## 2024-05-22 - CLI Flags are Essential UX
**Learning:** Even internal CLI tools are "user interfaces". Missing standard flags like `-h` or `--help` causes immediate confusion and errors (e.g., interpreting `-h` as a version argument).
**Action:** Always implement a basic `show_help` function and argument parsing for standard flags in shell scripts, regardless of how simple the script is.

## 2024-05-22 - Actionable Error Messages
**Learning:** Silent failures (like `yq` failing to update config) leave users in an inconsistent state without knowing why.
**Action:** Detect tool failures and provide specific, manual fallback instructions ("Please manually add detected languages...") instead of failing silently or crashing.
