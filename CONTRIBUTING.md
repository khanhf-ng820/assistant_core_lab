
# Contributing Guidelines

Thank you for contributing to the Study Assistant project.

## Development Workflow

1. Create or assign yourself to a GitHub Issue.
2. Create a dedicated branch from the latest `main`.
3. Implement changes and add appropriate tests.
4. Run the test suite before committing.
5. Open a Pull Request linked to the Issue.
6. Request a review and address all feedback before merging.

## Testing

Run the automated tests before submitting a Pull Request:

```bash
python -m pytest -q
```

All tests must pass before merging.

## Secrets

Never commit sensitive information to the repository.

- Do not commit API keys, passwords, access tokens, or credentials.
- Store local secrets in `.env`, which is excluded by `.gitignore`.
- Use `.env.example` to document configuration variables with safe placeholders.
- Never include real credentials in `.env.example`.
- Do not expose secrets in source code, tests, logs, documentation, or Pull Requests.
- Review staged changes before committing to prevent accidental exposure.

### Environment Configuration

Copy `.env.example` to `.env` when local environment configuration is required.

Only add real credentials to your local `.env` file.
The current rule-based assistant does not require an API key.

### If a Secret Is Exposed

1. Revoke or rotate the compromised credential immediately.
2. Notify the repository maintainer.
3. Remove the exposed secret from the affected files.
4. Coordinate with the maintainer if Git history needs to be cleaned.
5. Verify that the compromised credential can no longer be used.

Removing a secret from the latest commit does not make an exposed credential safe.
