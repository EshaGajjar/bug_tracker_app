# DevTrack (Issue Tracker API)

A minimal backend API for tracking engineering issues (reporters file issues, set priority, and track status).

## How to run

```bash
cd devtrack
python3 -m venv .venv
source .venv/bin/activate
pip install django djangorestframework
python3 devtrack/manage.py runserver
```

- Server runs at **`http://127.0.0.1:8000/`**

## Data storage (JSON)

Data is stored in two JSON files:

- `devtrack/devtrack/issue_tracker/data/reporters.json`
- `devtrack/devtrack/issue_tracker/data/issues.json`

## OOP model classes

OOP classes are implemented in **`devtrack/devtrack/issue_tracker/models.py`**:

- `BaseEntity` (abstract): `validate()` + `to_dict()`
- `Reporter`
- `Issue`, `CriticalIssue`, `LowPriorityIssue`

Views only **import** these classes; they are **not** defined inside `views.py`.

## API Endpoints

### Reporters

- **GET** `http://127.0.0.1:8000/api/reporters/`  
  Returns all reporters.

- **POST** `http://127.0.0.1:8000/api/reporters/`  
  Creates a reporter.

  Example JSON body:

```json
{
  "name": "Ada Lovelace",
  "email": "ada@company.com",
  "team": "backend"
}
```

- **GET** `http://127.0.0.1:8000/api/reporters/<id>/`  
  Returns reporter details by id.

### Issues

- **GET** `http://127.0.0.1:8000/api/issues/`  
  Returns all issues.

- **POST** `http://127.0.0.1:8000/api/issues/`  
  Creates an issue. For `priority=critical` it uses `CriticalIssue`; for `priority=low` it uses `LowPriorityIssue`; otherwise base `Issue`.

  Example JSON body:

```json
{
  "title": "Login breaks on Safari",
  "description": "Users cannot login on Safari 17.x",
  "status": "open",
  "priority": "critical",
  "reporter_id": 1
}
```

- **GET** `http://127.0.0.1:8000/api/issues/<id>/`  
  Returns issue details by id.

- **GET** `http://127.0.0.1:8000/api/issues/status/<status>/`  
  Filters issues by status (case-insensitive).

  Example: `.../api/issues/status/open/`

## Postman testing (screenshots required)

Add screenshots to your repo and link them here.

### Reporters

- **Success screenshot**: `docs/postman/reporters_success.png`
- **Failure screenshot**: `docs/postman/reporters_failure.png`

Suggested failure test:
- POST reporter with invalid email (missing `@`) → should fail validation

### Issues

- **Success screenshot**: `docs/postman/issues_success.png`
- **Failure screenshot**: `docs/postman/issues_failure.png`

Suggested failure tests:
- POST issue with invalid `status` (not in `open/in_progress/resolved/closed`)
- POST issue with `reporter_id` that doesn’t exist

## One design decision

**Chose JSON file storage (`reporters.json` / `issues.json`) instead of a DB** to keep the project minimal and easy to test without migrations. This matches the assignment constraints while still allowing persistence across server restarts.

