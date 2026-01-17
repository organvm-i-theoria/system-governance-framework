## 2024-05-22 - CLI UX Patterns
**Learning:** CLI tools often lack basic usability features like help flags, leading to user confusion where flags are interpreted as arguments.
**Action:** Always implement a `show_help` function and check for `-h`/`--help` *before* processing positional arguments in shell scripts.

## 2024-05-22 - Interactive Prompt Accessibility
**Learning:** Standard `read -p` prompts often lack visual distinction, making them hard to spot in verbose logs.
**Action:** Use `echo -ne "${YELLOW}Question? ${NC}"` followed by `read -n 1` to create consistent, accessible, and visually distinct prompts.
