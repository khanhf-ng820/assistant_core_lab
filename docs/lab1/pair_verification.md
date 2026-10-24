# Lab 1 — Pair Verification Sheet

## Participants

| Role | Name | Student ID | Team |
|------|------|------------|------|
| Repository owner | Nguyễn Phúc Khánh | 25125086 | Team 07 |
| Verifier (partner) | Võ Gia Minh | 25125030 | Group 04 |

- **Repository verified:** `https://github.com/khanhf-ng820/assistant-team07.git`
- **Partner repository:** `https://github.com/MorganConsort/lab01-group04.git`
- **Date:** 2026-10-11
- **OS / Python version:** macOS / Python 3.14 (and verified compatibility with Python 3.10+)

---

## Rules Followed

- [x] Cloned the repository into a **new, empty folder**
- [x] Followed **only the README** (no talking, no pointing, no outside help)

---

## Timing

| Milestone | Time |
|-----------|------|
| Start (git clone) | 16:45 |
| Finish (tests passing) | 16:49 |
| **Total** | **4 min** |

**Under 10 minutes?** &nbsp; [x] Yes &nbsp; [ ] No

---

## Course Standard Verification Table

| Step in README | Worked? (Y/N) | Time | What was unclear or missing |
|---|---|---|---|
| Clone | Y | 1 min | Added HTTPS clone option alongside SSH for users without SSH keys configured |
| Create environment | Y | 1 min | None |
| Install dependencies | Y | 1 min | None |
| Run the app | Y | 0.5 min | None |
| Run the tests | Y | 0.5 min | Updated expected output to "6 passed" to reflect added office tests |
| `python scripts/check_env.py` all OK | Y | 0.5 min | None |

**Total time:** 4 min (target: under 10 min)

---

## Step-by-Step Checklist

| # | README Step | Worked as written? | Notes / Command output |
|---|-------------|--------------------|------------------------|
| 1 | `git clone ...` and `cd assistant-team07` | [x] Yes [ ] No | Successfully cloned into fresh directory |
| 2 | Create virtual environment (`python3 -m venv .venv`) | [x] Yes [ ] No | Isolated environment created |
| 3 | Activate virtual environment (`source .venv/bin/activate`) | [x] Yes [ ] No | Active prefix `(.venv)` appeared |
| 4 | Upgrade pip & install dependencies (`pip install -r requirements.txt`) | [x] Yes [ ] No | Pinned pytest installed cleanly |
| 5 | Install package in editable mode (`pip install -e .`) | [x] Yes [ ] No | `assistant` installed in editable mode |
| 6 | Run environment checker (`python scripts/check_env.py`) | [x] Yes [ ] No | All checks passed `[ OK ]` |
| 7 | Run assistant CLI query (`python -m assistant "where is the training office?"`) | [x] Yes [ ] No | Output matched expected string |
| 8 | Run automated tests (`pytest -q`) | [x] Yes [ ] No | All 6 smoke tests passed |

---

## Actual Outputs

### 1. Run step output
```
Training Office: room I.101, open Mon-Fri 07:30-16:30.
```

### 2. Test step output
```
......                                                                   [100%]
6 passed in 0.04s
```

### 3. Environment check output
```
[ OK ] Python >= 3.10 (found 3.14.7)
[ OK ] running inside a virtual environment
[ OK ] pytest installed
[ OK ] git available
[ OK ] inside a git repository
[ OK ] .gitignore present
[ OK ] README has no TODO left
[ OK ] git user.email set (ngpkhanh08@gmail.com)
[ OK ] starter app imports and answers

All good!
```

---

## Problems Found & Fixes Made by Owner

| # | Problem / Feedback | Fix Applied | Commit Hash |
|---|--------------------|-------------|-------------|
| 1 | Initial README only provided SSH clone URL (`git@github.com:...`), which fails if the partner hasn't set up GitHub SSH keys. | Added HTTPS clone command (`https://github.com/khanhf-ng820/assistant-team07.git`) alongside SSH in the Setup section. | `ac5799e` |
| 2 | Test section stated `Expected result: all unit tests pass (e.g., 4 passed)`, but step 6 added two new tests. | Updated expected test count in README to `6 passed`. | `ac5799e` |

---

## Mutual Verification Note

- Verifier's team repo ([`MorganConsort/lab01-group04`](https://github.com/MorganConsort/lab01-group04)) was also cloned into a clean isolated folder and verified following their README:
  - Setup and dependencies installed cleanly.
  - Test suite passed with `6 passed in 0.06s`.
  - Assistant query `python -m assistant "where is the library?"` returned `Library: room B.201, open Mon-Sat 07:00-20:00`.

---

## Verdict

- [x] **PASS WITH FIXES** — clone to passing tests in under 10 minutes (actual: 4 minutes); minor documentation clarity improvements committed.

**Verifier comments:**
> Setup was quick and straightforward. Instructions in README were clear and reproducible from a fresh directory.
