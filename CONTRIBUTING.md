# Contributing to CyberShield

Thank you for your interest in contributing!

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-user/cybershield.git`
3. Create a branch: `git checkout -b feat/your-feature`
4. Set up the environment:

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
```

## Running locally

```bash
make dev
# or
uvicorn app.main:app --reload
```

## Running tests

```bash
make test
```

## Commit conventions

Use conventional commits:
- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation changes
- `chore:` maintenance tasks
- `test:` adding or fixing tests
- `refactor:` code refactoring
- `perf:` performance improvements
- `ci:` CI/CD changes

## Pull Request process

1. Make sure all tests pass
2. Update the README if needed
3. Update the CHANGELOG under [Unreleased]
4. Open a Pull Request with a clear description

## Reporting bugs

Open an issue with:
- Description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment (OS, Python version)
