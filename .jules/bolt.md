## 2026-01-17 - [Batching Shell Processes]
**Learning:** Shell loops that invoke external binaries (like `yq`) create significant overhead due to repeated process forking.
**Action:** Always look for ways to batch operations into a single binary call (e.g. constructing a JSON list for `yq` or using `xargs`).
