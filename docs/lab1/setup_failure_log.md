# Lab 1 Setup Failure and Recovery Log (Homework H1)

**Student Name:** Đặng Xuân Phát  
**Student ID / Member No:** Member 4 (Team 07)  
**Repository:** `lab01-phatdx` / `assistant-team07`  
**Date:** October 10, 2026  

---

## 1. Objective
The purpose of this exercise is to intentionally simulate virtual environment and configuration failures ("break your setup"), and verify that the environment can be fully recovered by following **only** the instructions documented in `README.md`.

---

## 2. Failure Scenarios and Recovery Log

### Incident 1: Virtual Environment Deletion & Missing Module Error
* **Action Taken to Break Setup:** Deleted the `.venv` directory and uninstalled pytest from global scope.
  ```powershell
  Remove-Item -Recurse -Force .venv
  ```
* **Observed Error Message:**
  ```text
  ModuleNotFoundError: No module named 'assistant'
  # or when running pytest:
  pytest : The term 'pytest' is not recognized as the name of a cmdlet, function, script file, or operable program.
  ```
* **Root Cause Analysis:** The isolated Python environment was missing, causing Python to fallback to system interpreter where `assistant` package (editable mode) and dependencies were not installed.
* **Recovery Procedure Executed (following `README.md`):**
  ```powershell
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  python -m pip install --upgrade pip
  pip install -r requirements.txt
  pip install -e .
  ```
* **Verification Command & Result:**
  ```powershell
  pytest -q
  # Output: 4 passed in 0.02s
  python scripts/check_env.py
  # Output: All checks [ OK ]
  ```

---

### Incident 2: PowerShell Script Execution Policy Restriction
* **Action Taken to Break Setup:** Reset PowerShell execution policy to default `Restricted`.
  ```powershell
  Set-ExecutionPolicy -Scope CurrentUser Restricted
  ```
* **Observed Error Message:**
  ```text
  File C:\...\assistant-team07\.venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled on this system.
  ```
* **Root Cause Analysis:** Windows PowerShell security policy prevents unsigned script execution by default.
* **Recovery Procedure Executed (following `README.md` Troubleshooting section):**
  ```powershell
  Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
  ```
* **Verification Result:** `.venv\Scripts\Activate.ps1` executed successfully, prefix `(.venv)` appeared in prompt.

---

## 3. Conclusion & README Adjustments
Following the recovery steps in `README.md` restored the project environment to 100% operational status without requesting outside help. A troubleshooting note for PowerShell script execution was confirmed to be accurate and complete.
