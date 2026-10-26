# Study Assistant — starter

A rule-based study assistant for the CSC10014 Smart Virtual Assistant project. It helps students find campus office locations and operational hours from the command line.

## Prerequisites

- Python >= 3.10
- Git

## Setup

Clone the repository and prepare your isolated virtual environment:

```bash
# Clone via HTTPS (recommended) or SSH
git clone https://github.com/khanhf-ng820/assistant_core_lab.git
# or: git clone git@github.com:khanhf-ng820/assistant_core_lab.git
cd assistant_core_lab
python3 -m venv .venv
source .venv/bin/activate  # On Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

Verify the installation:

```bash
python -m assistant_core "where is the training office?"
```

## Run

Ask a single question directly via the command line:

```bash
python -m assistant_core "where is the training office?"
# Output: Training Office: room I.101, open Mon-Fri 07:30-16:30.
```

Or enter interactive mode (type `quit` or `exit` to leave):

```bash
python -m assistant_core
# Study assistant core (interactive mode). Type 'quit' or 'exit' to exit.
# > hi
# Hello! I can help with offices, fees and rules.
# > quit
```


### Supported queries

- Greetings: `hi`, `hello`, `hey`, `xin chao`, ...
- Office lookup: `where is the library?`
- Tuition: `tuition for 18 credits and 2 retake`
- Handbook rules: `thesis registration credits`

## Test

Run automated smoke tests using pytest:

```bash
pytest -q
```

Expected result: all unit tests pass.

## Evaluate

Lab 2 benchmark artifacts (`eval/cases.csv`, `eval/run.py`) are not shipped with this repository.

## Project structure

- `data/`: Sample datasets (`offices.csv`, `handbook.json`).
- `docs/`: Project documentation, reports, and worksheets.
- `lab03/`: Lab 3 monolith (intentionally non-compliant) and worksheets.
- `src/assistant_core/`: Core application package.
- `tests/`: Automated unit tests.

## Troubleshooting

- **`No module named assistant_core`**: Ensure the virtual environment is active (`source .venv/bin/activate`) and you installed the package in editable mode with `pip install -e .`.
- **PowerShell blocks script execution on Windows**: Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` before running `.venv\Scripts\Activate.ps1`, or use Git Bash.
- **Python command not found**: On macOS/Linux, try `python3`; on Windows, try `py`.
