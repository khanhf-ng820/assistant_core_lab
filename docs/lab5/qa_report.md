
# Lab 5 — Persistence Verification Report

**Student:** Nguyen Minh Khang
**Student ID:** 25125018
**GitHub:** @KaKaAkagami
**Role:** QA/QC
**Branch:** test/persistence-verification

## 1. Objective

Verify that SQLite preserves interaction and feedback records after closing and reopening the database.

Additionally, assess whether feedback survives an actual API server restart.

## 2. Test Environment

- Repository: khanhf-ng820/assistant_core_lab
- Python: 3.13
- Database: SQLite
- ORM: SQLModel
- Test framework: pytest
- Static analysis: Ruff

## 3. Test Cases

| Test | Description | Result on R1 |
|---|---|---|
| Interaction persistence | Record interaction, dispose engine, reopen database, verify saved data | PASS |
| Feedback persistence | Record feedback, dispose engine, reopen database, verify rating and comment | PASS |

Both tests use temporary file-backed SQLite databases to ensure data is persisted to disk.

## 4. Test Results

### Baseline — main

Commit: `fd398ca`

Results:
- 1 passed
- 1 failed

Failure: `NotImplementedError("R1")`

Evidence: [Baseline test log](persistence_test_log.txt)

### R1 Implementation

Commit: `3571f2c`

Results:
- 2 passed
- 0 failed

Evidence: [R1 passing test log](persistence_r1_pass_log.txt)

### R1 Full Regression

Results:
- 222 passed
- 4 skipped
- 0 failed

Ruff: All checks passed.

## 5. API Server Restart Verification

**Status: PENDING**

At the time of testing, the root API still uses an in-memory `feedback_store`.

The API does not yet persist feedback through `Repository.add_feedback()`.

Therefore, reopening SQLite successfully does not prove that feedback survives an actual Uvicorn restart.

The final integration must be verified by:

1. Starting the API with a file-backed SQLite database.
2. Creating an interaction and submitting feedback.
3. Stopping the API server.
4. Starting a new API server process with the same database file.
5. Retrieving the feedback and confirming its data remains unchanged.

## 6. Outstanding Dependencies

- Merge R1 `add_feedback()`.
- Implement and integrate R2 `list_feedback()`.
- Connect HTTP endpoints to SQLite.
- Repeat persistence tests on final `main`.
- Capture server restart test logs and screenshots.

## 7. Conclusion

Interaction and feedback persistence passed the database-reopen tests on the R1 implementation.

The server restart requirement remains unverified until the HTTP API is integrated with SQLite.

This report documents partial QA acceptance, not final Lab 5 acceptance.
