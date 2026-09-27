# BNPL

A small BNPL project based on a microservices and event-driven architecture.

## Local Development — Service Initialization

Each microservice has its own Python environment, `pyproject.toml`, lock file, and dependencies managed with `uv`.

### Initialize a new service

From an empty service directory:

```bash
cd services/<service-name>
```

Install the required Python version if it is not already available:

```bash
uv python install 3.12
```

Initialize the project with the required Python version:

```bash
uv init --python 3.12
```

Create the virtual environment and synchronize dependencies:

```bash
uv sync
```

Verify the Python version:

```bash
uv run python --version
```

### Add dependencies

Add runtime dependencies with:

```bash
uv add <package>
```

For example:

```bash
uv add fastapi "uvicorn[standard]"
```

Add development-only dependencies with:

```bash
uv add --dev <package>
```

For example:

```bash
uv add --dev pytest ruff
```

### Run commands

Prefer running Python commands through `uv`:

```bash
uv run python
uv run pytest
uv run uvicorn app.main:app --reload
```

Manual activation of `.venv` is not required.

### General rule

Every microservice must maintain its own environment and dependency configuration:

```text
services/<service-name>/
├── .venv/              # Local only, do not commit
├── .python-version
├── pyproject.toml
├── uv.lock
└── ...
```

Do not share a virtual environment or `pyproject.toml` between microservices.

Commit `.python-version`, `pyproject.toml`, and `uv.lock` to Git. Do not commit `.venv/`.
