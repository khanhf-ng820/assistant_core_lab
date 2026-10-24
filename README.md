# Study Assistant — starter

A rule-based study assistant for the CSC10014 Smart Virtual Assistant project. It helps students find campus office locations and operational hours from the command line.

## Prerequisites

- Python >= 3.10
- Git

## Setup

Clone the repository and prepare your isolated virtual environment:

```bash
# Clone via HTTPS (recommended) or SSH
git clone https://github.com/khanhf-ng820/assistant-team07.git
# or: git clone git@github.com:khanhf-ng820/assistant-team07.git
cd assistant-team07
python3 -m venv .venv
source .venv/bin/activate  # On Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

Verify your environment configuration:

```bash
python scripts/check_env.py
```

## Run

Ask a single question directly via the command line:

```bash
python -m assistant "where is the training office?"
# Output: Training Office: room I.101, open Mon-Fri 07:30-16:30.
```

Or enter interactive mode (type `quit` to exit):

```bash
python -m assistant
# Study assistant (starter). Type 'quit' to exit.
# > hi
# Hello! Ask me where an office is, or when it opens.
# > quit
```


### Help Command

The assistant provides a built-in `help` command to display
its supported features and usage instructions.

Run the help command directly:

```bash
python -m assistant "help"
```

Expected output:

```text
I can help you find offices and their opening hours. Try 'where is the library?'
```

The help command is case-insensitive and accepts extra
whitespace or trailing punctuation.

You can also use it in interactive mode:

```text
> help
I can help you find offices and their opening hours. Try 'where is the library?'
```

## Test

Run automated smoke tests using pytest:

```bash
pytest -q
```

Expected result: all unit tests pass (e.g., `13 passed`).

## Evaluate

Run the accuracy benchmark against `eval/cases.csv`:

```bash
python eval/run.py
```

Expected output when all benchmark answers match: `Accuracy: 15/15 (100.0%)`.

## Project structure

- `data/`: Small, non-sensitive sample datasets (`offices.csv`).
- `docs/`: Project documentation, reports, and worksheets.
- `scripts/`: Development and environment helper scripts (`check_env.py`).
- `src/`: Core application package (`assistant`).
- `tests/`: Automated unit and smoke test suites (`test_smoke.py`).
- `ui/`: User interface components and documentation.

## Troubleshooting

- **`No module named assistant`**: Ensure the virtual environment is active (`source .venv/bin/activate`) and you installed the package in editable mode with `pip install -e .`.
- **PowerShell blocks script execution on Windows**: Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` before running `.venv\Scripts\Activate.ps1`, or use Git Bash.
- **Python command not found**: On macOS/Linux, try `python3`; on Windows, try `py`.
- **Environment check failure**: Run `python scripts/check_env.py` to identify missing packages or configuration errors.
