"""SkillOps triage: the agent drafts, this module decides.

The manager agent turns a chat message into a JSON draft. This module checks
the draft, works out what is missing, sets the risk from the person's own
words, picks the workflow, tracks the request's state and renders the reply
the agent posts in the room. Nothing here runs commands.

Usage (the manager agent runs this):
    python skillops/triage.py new [--id SKO-0001] < draft.json
    python skillops/triage.py show SKO-0001
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

STATE_DIR = Path(__file__).resolve().parent.parent / "state" / "requests"

TYPES = ("bug", "feature", "ui", "review")
TEXT_FIELDS = {"request_text": 4000, "summary": 200, "expected": 1000,
               "actual": 1000, "source_message_id": 200}
LIST_FIELDS = ("acceptance_criteria", "steps_to_reproduce")
REQUIRED = ("request_text", "summary", "type")

# Words that make a request high risk wherever they appear in the person's text.
HIGH_RISK = re.compile(
    r"\b(deploy\w*|production|prod|delet\w*|drop|rm\s+-rf|auth\w*|login|password\w*|"
    r"secret\w*|token\w*|credential\w*|payment\w*|billing|migrat\w*|permission\w*|"
    r"api[ _-]?key\w*)\b",
    re.IGNORECASE,
)

WORKFLOWS = {
    "bug-tdd": {
        "steps": "reproduce → failing regression test → fix → run tests → review",
        "outputs": ["reproduction", "regression test", "fix", "test results", "review notes"],
    },
    "feature-plan-tdd": {
        "steps": "confirm acceptance criteria → plan → tests first → implement → review",
        "outputs": ["plan", "tests", "implementation", "test results", "review notes"],
    },
    "ui-change": {
        "steps": "inspect current UI → user flow → accessibility and responsive checks → implement → visual review",
        "outputs": ["before/after notes", "accessibility check", "implementation", "review notes"],
    },
    "code-review": {
        "steps": "read the diff → run tests → security checks → findings",
        "outputs": ["findings with file references", "test results"],
    },
    "human-direction": {
        "steps": "stop; a person decides the next step before any change is made",
        "outputs": ["the reason this was stopped"],
    },
}
ROUTES = {"bug": "bug-tdd", "feature": "feature-plan-tdd", "ui": "ui-change", "review": "code-review"}

TRANSITIONS = {
    "RECEIVED": {"TRIAGED", "NEEDS_CLARIFICATION"},
    "NEEDS_CLARIFICATION": {"TRIAGED", "NEEDS_CLARIFICATION"},
    "TRIAGED": {"PLANNED", "NEEDS_CLARIFICATION"},
    "PLANNED": {"IMPLEMENTING"},
    "IMPLEMENTING": {"QA_REVIEW"},
    "QA_REVIEW": {"AWAITING_HUMAN_APPROVAL", "IMPLEMENTING"},
    "AWAITING_HUMAN_APPROVAL": {"APPROVED", "CHANGES_REQUESTED", "REJECTED"},
    "CHANGES_REQUESTED": {"IMPLEMENTING"},
    "APPROVED": {"COMPLETED"},
}


class DraftError(ValueError):
    pass


class TransitionError(ValueError):
    pass


def parse_draft(text):
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise DraftError(f"draft is not JSON: {exc.msg}") from None
    if not isinstance(data, dict):
        raise DraftError("draft must be a JSON object")
    unknown = set(data) - set(TEXT_FIELDS) - set(LIST_FIELDS) - {"type"}
    if unknown:
        raise DraftError(f"fields not allowed in a draft: {', '.join(sorted(unknown))} "
                         "(risk, workflow and status are decided by SkillOps)")
    for key in REQUIRED:
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise DraftError(f"'{key}' is required")
    if data["type"] not in TYPES:
        raise DraftError(f"'type' must be one of {', '.join(TYPES)}")
    for key, limit in TEXT_FIELDS.items():
        if key in data and (not isinstance(data[key], str) or len(data[key]) > limit):
            raise DraftError(f"'{key}' must be text of at most {limit} characters")
    for key in LIST_FIELDS:
        value = data.get(key, [])
        if not (isinstance(value, list) and len(value) <= 20
                and all(isinstance(i, str) and 0 < len(i) <= 500 for i in value)):
            raise DraftError(f"'{key}' must be a list of up to 20 short texts")
        data[key] = value
    return data


def assess(draft):
    """Missing information, risk and workflow for a valid draft."""
    questions = []
    if draft["type"] == "bug" and not (
        draft["steps_to_reproduce"] or (draft.get("expected") and draft.get("actual"))
    ):
        questions.append("What are the steps to reproduce it, or what did you expect and what happened instead?")
    if draft["type"] in ("feature", "ui") and not draft["acceptance_criteria"]:
        questions.append("What acceptance criteria tell us it is done?")

    words = sorted({m.lower() for m in HIGH_RISK.findall(draft["request_text"])})
    if words:
        risk, workflow = "high", "human-direction"
        reason = f"high risk: the request mentions {', '.join(words)}, so a person decides before any change"
    else:
        risk = "medium" if draft["type"] in ("feature", "ui") else "low"
        workflow = ROUTES[draft["type"]]
        reason = f"a {draft['type']} with {risk} risk goes to {workflow}"
    return {
        "risk": risk,
        "questions": questions,
        "workflow": None if questions else {"id": workflow, "reason": reason, **WORKFLOWS[workflow]},
    }


def transition(record, status):
    if status not in TRANSITIONS.get(record["status"], ()):
        raise TransitionError(f"{record['id']}: {record['status']} cannot move to {status}")
    record["status"] = status
    record["history"].append({"status": status, "at": datetime.now(timezone.utc).isoformat()})


def load(request_id, state_dir=STATE_DIR):
    path = Path(state_dir) / f"{request_id}.json"
    if not re.fullmatch(r"SKO-\d{4}", request_id) or not path.exists():
        raise DraftError(f"no request {request_id}")
    return json.loads(path.read_text(encoding="utf-8"))


def save(record, state_dir=STATE_DIR):
    record = {k: v for k, v in record.items() if k != "duplicate"}
    (Path(state_dir) / f"{record['id']}.json").write_text(json.dumps(record, indent=2), encoding="utf-8")


def submit(draft_text, state_dir=STATE_DIR, request_id=None):
    """Triage a draft as a new request, or as an answer to `request_id`."""
    draft = parse_draft(draft_text)
    state_dir = Path(state_dir)
    state_dir.mkdir(parents=True, exist_ok=True)
    # ponytail: linear scan of every record; fine for a demo, index by message id if it grows
    existing = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(state_dir.glob("SKO-*.json"))]

    if request_id:
        record = load(request_id, state_dir)
    else:
        msg = draft.get("source_message_id")
        dup = next((r for r in existing if msg and r.get("source_message_id") == msg), None)
        if dup:
            return {**dup, "duplicate": True}
        record = {"id": f"SKO-{len(existing) + 1:04d}", "status": "RECEIVED",
                  "history": [{"status": "RECEIVED", "at": datetime.now(timezone.utc).isoformat()}]}

    result = assess(draft)
    record.update(draft)
    record.update(result)
    transition(record, "NEEDS_CLARIFICATION" if result["questions"] else "TRIAGED")
    save(record, state_dir)
    return {**record, "duplicate": False}


def render(record):
    """The reply the agent posts in the room (Mattermost Markdown)."""
    lines = [f"**{record['id']}** · {record['type']} · risk **{record['risk']}** · `{record['status']}`",
             f"> {record['summary']}"]
    if record.get("duplicate"):
        lines.append("_Already tracked; this is the existing request._")
    if record["acceptance_criteria"]:
        lines += ["**Acceptance criteria**"] + [f"- {c}" for c in record["acceptance_criteria"]]
    if record["status"] == "NEEDS_CLARIFICATION":
        lines += ["**Before I can route this:**"] + [f"- {q}" for q in record["questions"]]
    elif record["workflow"]:
        wf = record["workflow"]
        lines += [f"**Workflow:** `{wf['id']}`: {wf['steps']}",
                  f"**Why:** {wf['reason']}",
                  f"**Expected outputs:** {', '.join(wf['outputs'])}"]
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="triage")
    sub = parser.add_subparsers(dest="cmd", required=True)
    new = sub.add_parser("new", help="triage a JSON draft read from stdin")
    new.add_argument("--id", help="answer to an existing request, e.g. SKO-0001")
    show = sub.add_parser("show", help="print a request")
    show.add_argument("id")
    args = parser.parse_args(argv)
    sys.stdin.reconfigure(encoding="utf-8")  # the manager sends UTF-8; Windows defaults to cp1252
    try:
        record = submit(sys.stdin.read(), request_id=args.id) if args.cmd == "new" else load(args.id)
    except (DraftError, TransitionError) as exc:
        print(f"Triage refused: {exc}", file=sys.stderr)
        return 2
    sys.stdout.reconfigure(encoding="utf-8")
    print(render(record))
    return 0


if __name__ == "__main__":
    sys.exit(main())
