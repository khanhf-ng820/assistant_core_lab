# Lab 7 — L1 show sources evidence

Owner: Trần Thành Lợi (25125059)
Reviewer: Lý Tuấn Kiệt (25125022)
Code: `lab07/starter/ui/logic.py` — `format_sources` (tutorial D.1)
Test: `lab07/starter/tests/test_ui.py::test_format_sources`

## What changed

`format_sources(sources)` returns `""` when the answer has no sources, otherwise
`"Sources: <id> — <title>"`, joined with `"; "` when there are several. `ui/app.py`
already stores this string per message and shows it with `st.caption` under the answer,
so no page change was needed.

## Result

```bash
cd lab07/starter
.venv/bin/python -m pytest -q tests/test_ui.py   # 7 passed
.venv/bin/python -m pytest -q                    # 49 passed
cd ../practice
../starter/.venv/bin/python -m pytest -q         # 4 passed
```

## End-to-end check (real API)

API started with `uvicorn assistant_api.main:create_app --factory`, then the UI client
(`ui.api_client.AssistantClient`) asked three questions:

| Question | `format_sources(result.sources)` |
|---|---|
| Can I register my thesis with 118 credits? | `Sources: H26#5.3 — 5.3 Thesis registration` |
| Where is the library? | `""` (no caption shown) |
| what is the capital of France | `""` (escalation note shown instead) |

This matches D.4 row 2 ("answer + `Sources: H26#5.3 — …`"). The browser screenshot for
D.4 is recorded by the D.4 runner in [`d4_acceptance.md`](d4_acceptance.md).

## AI use

Claude Code wrote the three-line implementation from the tutorial's D.1 snippet and ran
the tests and the API check. I read the change, confirmed it matches D.1, and verified the
test output above.
