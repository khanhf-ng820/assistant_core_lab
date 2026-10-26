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
| **24/10/2026** | Trần Phúc Khánh (Lab 3 follow-up, PR #6) | OpenAI Codex | Check PR #2 and fix the remaining old-package test imports | Changed legacy test imports to assistant_core.rules; preserved legacy office assertions using injected test data; skip benchmark tests only while both Lab 2 assets are absent | Codex inspected PR #2 and the diff; full suite: 34 passed, 4 skipped (missing benchmark artifacts); Ruff lint/format passed for the six changed Python files. Human author/reviewer inspection pending |
| **24/10/2026** | Trần Phúc Khánh (Lab 3, Member 2) | OpenAI Codex | Implement the assigned configuration and exception contract from the Lab 3 tutorial | Added named exceptions, typed environment settings, safe validation errors, a seven-variable .env.example, and focused tests; retained the tutorial defaults and provider/key rule | Codex inspected the diff: 18 focused tests passed; changed Python files passed Ruff lint/format. The initial full-suite run encountered two old assistant import errors (resolved in the follow-up above). Human author and reviewer inspection pending |
| **18/10/2026** | Trần Phúc Khánh (issue #9) | OpenAI Codex | Specify the future LLM interface without provider calls | Drafted `docs/ai-interface.md` with typed signatures, input/output contracts, errors, fallback, and local examples; added the docs index link | Codex executed the examples and regression suite; human author and reviewer inspection pending |
| **10/10/2026** | Đặng Xuân Phát | Gemini 3.6 Flash | Structure UI architecture & sitemap for `ui/README.md` | Adapted sitemap to HCMUS Q5 context; refined 6 screen wireframe specs | Manually checked against `Promptational Thinking.md` functional requirements |
| **10/10/2026** | Đặng Xuân Phát | Gemini 3.6 Flash | Draft setup failure recovery log `setup_failure_log.md` | Formatted error tracebacks for PowerShell & Python venv | Tested recovery script commands locally via terminal |
| **10/10/2026** | Đặng Xuân Phát | Gemini 3.6 Flash | Refactor Python Bootcamp W1 functions (`grades`, `text_tools`, `rules`, `translate`, `timetable`) | Added strict type hints, docstrings, and edge-case guards | Executed `pytest` suite locally; 24/24 unit tests passed (100% pass rate) |
| **18/10/2026** | Trần Phúc Khánh (issue #8) | OpenAI Codex | Document data sources, owners, and update frequency | Added a file inventory to `data/README.md`; retained sample-data status and existing security guidance | Codex checked the tracked inventory, CSV, loader, and regression suite; human author and reviewer inspection pending |
| **18/10/2026** | Lý Tuấn Kiệt | Gemini 3.8 Flash | Support partial office name lookup in backend (`rules.py`) | Implemented clean name and substring partial matching logic in `rules.py`; added unit tests in `test_smoke.py` | Ran pytest suite (15/15 passed), check_env.py, and manual CLI verification |
| **18/10/2026** | Lý Tuấn Kiệt | Gemini 3.8 Flash | Design how citations appear under answers (`docs/ui-sources.md`) | Drafted citation data schema, ASCII wireframes, Markdown mockups with 2 examples, and Streamlit implementation code | Verified Markdown rendering, reviewed alignment with Lab 02 acceptance criteria and DoD |
| **24/10/2026** | Nguyễn Phúc Khánh (issue #1) | Antigravity (Gemini 3.8 Flash) | Implement AssistantService, CLI, and architecture documentation for Lab 03 | Scaffolding for AssistantService with DI, CLI with structured JSON logging, docs/architecture.md, and test_service.py | Ran pytest suite (11/11 passed), ruff lint/format clean, manual CLI verification |
| **24/10/2026** | Trần Thành Lợi | OpenCode (DeepSeek) | Extract the Lab 3 responder adapter and test AI/provider failure paths | Added `responder.py` (`Responder` protocol, `TemplateResponder`, `StubLLMResponder`); rewired `service.py` to import it; added 22 offline tests for provider outage, citation preservation, logging hygiene, injected responders, and boundary validation | Ran `pytest` (30 passed, 4 optional benchmark tests skipped), `ruff check .` and `ruff format --check .` clean; human author review pending |
| **25/10/2026** | Lý Tuấn Kiệt (issue #13) | Antigravity (Gemini 3.8 Flash) | Implement pure tuition tools, credit parser, intent router, and characterisation tests | Implemented `src/assistant_core/tools.py`, `src/assistant_core/router.py`, `tests/test_tools.py`, `tests/test_router.py`, and integrated with `service.py` | Executed `pytest -v` (99 passed, 4 skipped); `ruff check .` clean (0 errors); verified legacy parity with monolith |
| **26/10/2026** | Lý Tuấn Kiệt (PR #14) | Antigravity (Gemini 3.8 Flash) | Address PR review comments: document `InvalidRequest` contract & add edge-case tests | Updated `docs/architecture.md`, `src/assistant_core/tools.py` docstrings, and added edge-case unit tests in `tests/test_tools.py` | Ran `pytest` suite (106 passed, 4 skipped); `ruff check .` clean (0 errors) |
| **26/10/2026** | Đặng Xuân Phát (Member 3) | Antigravity (Gemini 3.8 Flash) | Implement logging_setup.py and configure quality gates (pyproject.toml, requirements.txt) | Created logging_setup.py with JsonFormatter (structured logs to stderr, secret sanitization); pinned dependencies in requirements.txt; configured ruff rules in pyproject.toml; completed before/after maintainability worksheet | Ran pytest suite (106 passed, 4 skipped), ruff check . (clean), ruff check --select BLE . (clean), manual CLI test with stderr log redirect |

---

## 3. Human Inspection Protocol
Every AI-assisted contribution in this repository undergoes the following 3-step verification before committing:
1. **Inspect (`git diff`):** Verify every line of code generated to ensure no hallucinated packages, invalid API calls, or hidden security vulnerabilities exist.
2. **Verify (`pytest -q`):** Execute full test suite to guarantee that existing functionality remains unbroken.
3. **Disclose (`PR Description & AI Log`):** Document the tool used, prompt objective, and human modifications in the Pull Request body and this log file.
