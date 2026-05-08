import json
import os

from rest_framework.decorators import api_view
from rest_framework.views import Request, Response

from .models import CriticalIssue, Issue, LowPriorityIssue, Reporter

REPORTERS_FILE = (
    "/Users/gattu/Documents/Airtribe Python 🚀/DevTrack01/devtrack/devtrack/issue_tracker/data/reporters.json"
)

ISSUES_FILE = (
    "/Users/gattu/Documents/Airtribe Python 🚀/DevTrack01/devtrack/devtrack/issue_tracker/data/issues.json"
)


def read_data_from_file(file_path: str) -> list[dict]:
    try:
        with open(file_path, "r") as file:
            content = file.read()
            return json.loads(content) if content.strip() else []
    except FileNotFoundError:
        return []


@api_view(["GET", "POST"])
def reporters(request: Request):
    if request.method == "GET":
        reporters = read_data_from_file(REPORTERS_FILE)
        return Response(
            data={"message": "Reporters fetched", "data": reporters},
            status=200,
        )

    data = request.data
    reporter = Reporter(
        id=_get_next_reporter_id(),
        name=data["name"],
        email=data["email"],
        team=data["team"],
    )
    reporter.validate()
    create_reporter_in_file(reporter)
    return Response(
        data={"message": "Reporter created sucessfully", "data": reporter.__dict__},
        status=201,
    )


@api_view(["GET", "POST"])
def issues(request: Request):
    if request.method == "GET":
        issues = read_data_from_file(ISSUES_FILE)
        return Response(
            data={"message": "Issues fetched", "data": issues},
            status=200,
        )

    data = request.data

    if data["priority"] == "critical":
        issue = CriticalIssue(
            id=_get_next_issue_id(),
            title=data["title"],
            description=data["description"],
            status=data["status"],
            priority=data["priority"],
            reporter_id=data["reporter_id"],
        )
    elif data["priority"] == "low":
        issue = LowPriorityIssue(
            id=_get_next_issue_id(),
            title=data["title"],
            description=data["description"],
            status=data["status"],
            priority=data["priority"],
            reporter_id=data["reporter_id"],
        )
    else:
        issue = Issue(
            id=_get_next_issue_id(),
            title=data["title"],
            description=data["description"],
            status=data["status"],
            priority=data["priority"],
            reporter_id=data["reporter_id"],
        )
    issue.validate()

    reporters_data = read_data_from_file(REPORTERS_FILE)
    reporter_exists = any(
        isinstance(r, dict) and r.get("id") == issue.reporter_id for r in reporters_data
    )
    if not reporter_exists:
        return Response(data={"message": "Reporter not found for reporter_id"}, status=400)

    create_issue_in_file(issue)

    response_data = issue.to_dict()
    response_data["message"] = issue.describe()

    return Response(
        data={"message": "Issue created successfully", "data": response_data},
        status=201,
    )

def _get_next_reporter_id() -> int:
    reporters = read_data_from_file(REPORTERS_FILE)

    max_id = 0
    for r in reporters:
        rid = r.get("id", 0) if isinstance(r, dict) else 0
        if isinstance(rid, int) and rid > max_id:
            max_id = rid
    return max_id + 1


def create_reporter_in_file(reporter: Reporter):
    reporters = read_data_from_file(REPORTERS_FILE)

    reporters.append(reporter.__dict__)

    os.makedirs(os.path.dirname(REPORTERS_FILE), exist_ok=True)
    with open(REPORTERS_FILE, "w", encoding="utf-8") as file:
        file.write(json.dumps(reporters, default=str, indent=2))


@api_view(["GET"])
def get_reporter_details(request: Request, id: int):
    reporters = read_data_from_file(REPORTERS_FILE)

    reporter = next((r for r in reporters if isinstance(r, dict) and r.get("id") == id), None)
    if reporter is None:
        return Response(data={"message": "Reporter not found"}, status=404)

    return Response(data={"message": "Reporter fetched", "data": reporter}, status=200)


def _get_next_issue_id() -> int:
    issues = read_data_from_file(ISSUES_FILE)

    max_id = 0
    for i in issues:
        iid = i.get("id", 0) if isinstance(i, dict) else 0
        if isinstance(iid, int) and iid > max_id:
            max_id = iid
    return max_id + 1


def create_issue_in_file(issue: Issue):
    issues = read_data_from_file(ISSUES_FILE)

    issues.append(issue.__dict__)

    os.makedirs(os.path.dirname(ISSUES_FILE), exist_ok=True)
    with open(ISSUES_FILE, "w", encoding="utf-8") as file:
        file.write(json.dumps(issues, default=str, indent=2))


@api_view(["GET"])
def get_issue_details(request: Request, id: int):
    issues = read_data_from_file(ISSUES_FILE)

    issue = next((i for i in issues if isinstance(i, dict) and i.get("id") == id), None)
    if issue is None:
        return Response(data={"message": "Issue not found"}, status=404)

    return Response(data={"message": "Issue fetched", "data": issue}, status=200)


@api_view(["GET"])
def get_filtered_issue_details(request: Request, status: str):
    issues = read_data_from_file(ISSUES_FILE)

    filtered = [
        i
        for i in issues
        if isinstance(i, dict)
        and str(i.get("status", "")).lower() == str(status).lower()
    ]
    return Response(
        data={"message": "Filtered issues fetched", "data": filtered},
        status=200,
    )