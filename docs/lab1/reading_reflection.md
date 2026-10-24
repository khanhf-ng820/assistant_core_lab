# Reading Reflection Note (Homework H3)

**Student Name:** Đặng Xuân Phát (Member 4, Team 07)  
**Readings:** *MIT Missing Semester: Shell Tools and Scripting* & *GitHub Hello World*  

---

1. **One command I will use daily:**  
   `git status` (and `git diff`) — Essential for maintaining workspace awareness and inspecting staged/unstaged changes before every commit to ensure reproducible setups.

2. **One command I found surprising:**  
   `git reflog` — Surprising and reassuring to learn that Git maintains an immutable local journal of every `HEAD` position change, allowing recovery from accidental `git reset --hard` actions.

3. **One question:**  
   In collaborative team workflows with protected `main` branches, what is the best practice for managing pre-commit hooks (like `ruff` or `gitleaks`) across different operating systems (Windows PowerShell vs. macOS/Linux Bash) without causing line-ending (`CRLF` vs. `LF`) conflicts in Git diffs?
