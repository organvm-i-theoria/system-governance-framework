## 2024-03-21 - Missing Input Validation in Shell Scripts
**Vulnerability:** `scripts/install-framework.sh` accepted arbitrary input for `VERSION` and `PRESET` variables, allowing for potential command injection or path traversal.
**Learning:** Even if variables are quoted, they can be used in contexts (like file paths or URLs) where they can cause harm (path traversal). Input validation must be explicit and fail-fast.
**Prevention:** Implement regex-based allowlists for all script arguments and explicitly check for path traversal sequences like `..` immediately after variable assignment (and after color definitions if colors are used in error messages).
