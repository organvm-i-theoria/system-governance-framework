## 2024-05-23 - Batching yq operations
**Learning:** Calling `yq` inside a loop for array manipulation creates excessive process overhead in shell scripts.
**Action:** Construct JSON arrays using bash `printf` and pass a single payload to `yq` using the `+=` operator.
