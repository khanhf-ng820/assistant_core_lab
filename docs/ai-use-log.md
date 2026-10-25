# Academic AI Use Log & Integrity Disclosure

**Course:** CSC10014 - Computational Thinking (2026)  
**Team:** Team 07 (`assistant-team07`)  
**Document Maintenance:** All Team Members  

---

## 1. Academic AI Policy Compliance Statement

In accordance with the course policy for CSC10014, artificial intelligence tools (such as Copilot, Gemini, ChatGPT, Claude) are permitted as cognitive assistants provided their usage is **transparently disclosed**, **strictly audited by human authors**, and **thoroughly verified through unit tests**.

Undisclosed AI code generation is considered an academic integrity violation. Disclosed and human-verified AI assistance is welcome as part of modern developer workflows.

---

## 2. AI Usage Registry

| Date | Author | AI Tool | Task / Prompt Goal | Kept / Modified Code | Human Verification Method |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **18/10/2026** | Trần Phúc Khánh (issue #9) | OpenAI Codex | Specify the future LLM interface without provider calls | Drafted `docs/ai-interface.md` with typed signatures, input/output contracts, errors, fallback, and local examples; added the docs index link | Codex executed the examples and regression suite; human author and reviewer inspection pending |
| **10/10/2026** | Đặng Xuân Phát | Gemini 3.6 Flash | Structure UI architecture & sitemap for `ui/README.md` | Adapted sitemap to HCMUS Q5 context; refined 6 screen wireframe specs | Manually checked against `Promptational Thinking.md` functional requirements |
| **10/10/2026** | Đặng Xuân Phát | Gemini 3.6 Flash | Draft setup failure recovery log `setup_failure_log.md` | Formatted error tracebacks for PowerShell & Python venv | Tested recovery script commands locally via terminal |
| **10/10/2026** | Đặng Xuân Phát | Gemini 3.6 Flash | Refactor Python Bootcamp W1 functions (`grades`, `text_tools`, `rules`, `translate`, `timetable`) | Added strict type hints, docstrings, and edge-case guards | Executed `pytest` suite locally; 24/24 unit tests passed (100% pass rate) |
| **18/10/2026** | Trần Phúc Khánh (issue #8) | OpenAI Codex | Document data sources, owners, and update frequency | Added a file inventory to `data/README.md`; retained sample-data status and existing security guidance | Codex checked the tracked inventory, CSV, loader, and regression suite; human author and reviewer inspection pending |
| **18/10/2026** | Lý Tuấn Kiệt | Gemini 3.8 Flash | Support partial office name lookup in backend (`rules.py`) | Implemented clean name and substring partial matching logic in `rules.py`; added unit tests in `test_smoke.py` | Ran pytest suite (15/15 passed), check_env.py, and manual CLI verification |
| **18/10/2026** | Lý Tuấn Kiệt | Gemini 3.8 Flash | Design how citations appear under answers (`docs/ui-sources.md`) | Drafted citation data schema, ASCII wireframes, Markdown mockups with 2 examples, and Streamlit implementation code | Verified Markdown rendering, reviewed alignment with Lab 02 acceptance criteria and DoD |
| **24/10/2026** | Nguyễn Phúc Khánh (issue #1) | Antigravity (Gemini 3.8 Flash) | Implement AssistantService, CLI, and architecture documentation for Lab 03 | Scaffolding for AssistantService with DI, CLI with structured JSON logging, docs/architecture.md, and test_service.py | Ran pytest suite (11/11 passed), ruff lint/format clean, manual CLI verification |
| **25/10/2026** | Lý Tuấn Kiệt (issue #13) | Antigravity (Gemini 3.8 Flash) | Implement pure tuition tools, credit parser, intent router, and characterisation tests | Implemented `src/assistant_core/tools.py`, `src/assistant_core/router.py`, `tests/test_tools.py`, `tests/test_router.py`, and integrated with `service.py` | Executed `pytest -v` (99 passed, 4 skipped); `ruff check .` clean (0 errors); verified legacy parity with monolith |



---

## 3. Human Inspection Protocol
Every AI-assisted contribution in this repository undergoes the following 3-step verification before committing:
1. **Inspect (`git diff`):** Verify every line of code generated to ensure no hallucinated packages, invalid API calls, or hidden security vulnerabilities exist.
2. **Verify (`pytest -q`):** Execute full test suite to guarantee that existing functionality remains unbroken.
3. **Disclose (`PR Description & AI Log`):** Document the tool used, prompt objective, and human modifications in the Pull Request body and this log file.
