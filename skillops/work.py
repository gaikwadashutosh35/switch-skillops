"""SkillOps work: the gated steps after triage.

Each command checks the request's state before it acts, so an agent cannot
skip review or merge without a person's approval. Git and the tests run with
fixed arguments, never through a shell, and only in the demo repository.

Usage (agents run these; each prints the reply to post in the room):
    python skillops/work.py reset-demo                         # clears requests, recreates the demo repo
    python skillops/work.py start SKO-0001                     # manager
    python skillops/work.py check SKO-0001 [--expect fail]     # coder
    python skillops/work.py review SKO-0001 --verdict pass|changes --notes "..."   # reviewer
    python skillops/work.py decide SKO-0001 --by USER --message-id ID < message    # manager
    python skillops/work.py merge SKO-0001                     # manager, after APPROVED
"""

import argparse
import os
import re
import shutil
import stat
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

if __package__ in (None, ""):  # run as a script: python skillops/work.py
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from skillops import triage  # noqa: E402
from skillops.triage import STATE_DIR, TransitionError, load, save, transition  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SEED = ROOT / "demo" / "seed"
DEMO_REPO = ROOT / "workspace" / "demo-app"
TEST_COMMAND = [sys.executable, "-m", "unittest"]
AGENTS = {"skillops-manager", "skillops-coder", "skillops-reviewer"}
SECRET_NAME = r"[\w-]*(?:token|secret|passw(?:or)?d|api[_-]?key|authorization)[\w-]*"
REDACT = [
    # name=value, name: value, "name": "value", Authorization: Bearer value
    (re.compile(rf"(?i)\b({SECRET_NAME})([\"']?\s*[:=]\s*[\"']?)(?:(?:bearer|basic)\s+)?[^\s\"',}}]+"),
     r"\1\2[redacted]"),
    # Bearer value, --password value
    (re.compile(rf"(?i)(?<![\w-])(bearer|--{SECRET_NAME})(\s+)[^\s\"',}}]+"), r"\1\2[redacted]"),
    # well-known token shapes on their own
    (re.compile(r"\b(?:gh[pousr]_|github_pat_|xox[abprs]-|sk-|AKIA)[\w-]{8,}"), "[redacted]"),
    # user:password@ in a URL
    (re.compile(r"(://[^/\s:@]+:)[^@\s/]+@"), r"\1[redacted]@"),
]


class WorkError(RuntimeError):
    pass


class DecisionError(ValueError):
    pass


def now():
    return datetime.now(timezone.utc).isoformat()


def git(repo, *args):
    done = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, timeout=60)
    if done.returncode != 0:
        raise WorkError(f"git {args[0]} failed: {done.stderr.strip()}")
    return done.stdout.strip()


def reset_demo(repo=DEMO_REPO):
    """Recreate the demo repository from demo/seed: one commit on main."""
    repo = Path(repo).resolve()
    if repo.parent.name != "workspace":
        raise WorkError(f"refusing to reset {repo}: the demo repo must sit in a 'workspace' directory")
    if repo.exists():
        shutil.rmtree(repo, onexc=lambda fn, path, _: (os.chmod(path, stat.S_IWRITE), fn(path)))
    shutil.copytree(SEED, repo, ignore=shutil.ignore_patterns("__pycache__"))
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.name", "SkillOps demo")
    git(repo, "config", "user.email", "demo@skillops.local")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "Demo app: profile settings")
    return repo


def reset_state(state_dir=STATE_DIR):
    """Forget every request, so a demo run starts again at SKO-0001."""
    for path in Path(state_dir).glob("SKO-*.json"):
        path.unlink()


def run_tests(repo):
    try:
        # No bytecode: a check must never change the tree it is checking.
        env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
        done = subprocess.run(TEST_COMMAND, cwd=repo, env=env, capture_output=True, text=True, timeout=120)
        code, output = done.returncode, done.stdout + done.stderr
    except subprocess.TimeoutExpired:
        code, output = 124, "tests timed out after 120 seconds"
    tail = "\n".join(output.strip().splitlines()[-30:])
    return code, redact(tail)


def redact(text):
    for pattern, replacement in REDACT:
        text = pattern.sub(replacement, text)
    return text


def start(request_id, repo=DEMO_REPO, state_dir=STATE_DIR):
    """TRIAGED -> PLANNED, on a fresh branch in the demo repo."""
    record = load(request_id, state_dir)
    transition(record, "PLANNED")
    record["branch"] = f"sko-{request_id[4:]}"
    git(repo, "checkout", "-q", "main")
    git(repo, "checkout", "-q", "-B", record["branch"])
    save(record, state_dir)
    return record


def check(request_id, expect="pass", repo=DEMO_REPO, state_dir=STATE_DIR):
    """Run the tests on the request's branch and record the evidence."""
    record = load(request_id, state_dir)
    if record["status"] in ("PLANNED", "CHANGES_REQUESTED"):
        transition(record, "IMPLEMENTING")
    if record["status"] != "IMPLEMENTING":
        raise TransitionError(f"{request_id} is {record['status']}; checks run while IMPLEMENTING")
    if git(repo, "branch", "--show-current") != record["branch"]:
        raise WorkError(f"the demo repo is not on {record['branch']}")

    code, tail = run_tests(repo)
    dirty = git(repo, "status", "--porcelain")
    committed = git(repo, "diff", "--name-only", f"main...{record['branch']}").splitlines()
    if expect == "fail":
        note = "bug reproduced: tests fail" if code else "expected a failure, but the tests pass"
    elif code:
        note = "tests fail"
    elif dirty:
        note = "tests pass, but changes are not committed; commit them first"
    elif not committed:
        note = "tests pass, but the branch has no committed changes"
    else:
        note = "tests pass; ready for review"
        transition(record, "QA_REVIEW")
    record.setdefault("evidence", []).append({
        "at": now(), "command": "python -m unittest", "exit_code": code, "expect": expect,
        "note": note, "changed_files": committed, "output_tail": tail,
    })
    save(record, state_dir)
    return record


def review(request_id, verdict, notes, repo=DEMO_REPO, state_dir=STATE_DIR):
    """Reviewer's verdict; the tests are run again independently."""
    record = load(request_id, state_dir)
    if record["status"] != "QA_REVIEW":
        raise TransitionError(f"{request_id} is {record['status']}; reviews happen in QA_REVIEW")
    if verdict not in ("pass", "changes"):
        raise WorkError("verdict must be 'pass' or 'changes'")
    if git(repo, "branch", "--show-current") != record["branch"]:
        raise WorkError(f"the demo repo is not on {record['branch']}")
    if git(repo, "status", "--porcelain"):
        raise WorkError("the demo repo has uncommitted changes; only committed work is reviewed")
    commit = git(repo, "rev-parse", "HEAD")
    code, tail = run_tests(repo)
    if code:
        verdict, notes = "changes", f"tests fail on review. {notes}"
    record["review"] = {"at": now(), "verdict": verdict, "notes": notes, "commit": commit,
                        "exit_code": code, "output_tail": tail}
    if verdict == "pass":
        transition(record, "AWAITING_HUMAN_APPROVAL")
    else:
        record.setdefault("feedback", []).append({"at": now(), "by": "skillops-reviewer", "text": notes})
        transition(record, "IMPLEMENTING")
    save(record, state_dir)
    return record


def decide(request_id, message, by, message_id, repo=DEMO_REPO, state_dir=STATE_DIR):
    """Apply a person's decision, given their message word for word."""
    # ponytail: the agent reports the sender; trust it, but never accept an agent's own name
    if by in AGENTS or by.startswith(("skillops-", "switch")):
        raise DecisionError(f"{by} is an agent; only a person can decide")
    text = re.sub(r"^(\s*@\S+\s+)+", "", message).strip()
    hint = (f"Reply exactly `APPROVE {request_id} merge`, `CHANGES {request_id}: <what to change>` "
            f"or `REJECT {request_id}`.")
    approve = re.fullmatch(r"APPROVE\s+(SKO-\d{4})\s+merge", text, re.IGNORECASE)
    changes = re.fullmatch(r"CHANGES\s+(SKO-\d{4})\s*:\s*(.+)", text, re.IGNORECASE | re.DOTALL)
    reject = re.fullmatch(r"REJECT\s+(SKO-\d{4})(?:\s*:\s*(.*))?", text, re.IGNORECASE | re.DOTALL)
    match = approve or changes or reject
    if not match:
        raise DecisionError(f"not a decision. {hint}")
    if match.group(1).upper() != request_id:
        raise DecisionError(f"that decision is for {match.group(1).upper()}, not {request_id}")
    record = load(request_id, state_dir)
    if record["status"] != "AWAITING_HUMAN_APPROVAL":
        raise DecisionError(f"{request_id} is {record['status']}; nothing is waiting for a decision")
    entry = {"at": now(), "by": by, "message_id": message_id}
    if approve:
        record["approval"] = {**entry, "action": "merge"}
        transition(record, "APPROVED")
    elif changes:
        record.setdefault("feedback", []).append({**entry, "text": changes.group(2).strip()})
        transition(record, "CHANGES_REQUESTED")
    else:
        record["rejection"] = {**entry, "text": (reject.group(2) or "").strip()}
        transition(record, "REJECTED")
    save(record, state_dir)
    return record


def merge(request_id, repo=DEMO_REPO, state_dir=STATE_DIR):
    """Merge the approved branch into main: the one consequential action."""
    record = load(request_id, state_dir)
    if record["status"] != "APPROVED" or record.get("approval", {}).get("action") != "merge":
        raise WorkError(f"{request_id} is {record['status']}; merging needs `APPROVE {request_id} merge` "
                        "from a person first")
    reviewed = record.get("review", {}).get("commit")
    if not reviewed:
        raise WorkError(f"{request_id} has no reviewed commit to merge")
    git(repo, "checkout", "-q", "main")
    # The reviewed commit, not the branch: anything committed after review is not merged.
    git(repo, "merge", "-q", "--no-ff", reviewed, "-m",
        f"Merge {request_id}: {record['summary']} (approved by {record['approval']['by']})")
    record["merge"] = {"at": now(), "commit": git(repo, "rev-parse", "--short", "HEAD")}
    transition(record, "COMPLETED")
    save(record, state_dir)
    return record


NEXT = {
    "PLANNED": "Next: skillops-coder writes a failing regression test, then the fix.",
    "IMPLEMENTING": "Next: skillops-coder keeps working on the branch.",
    "QA_REVIEW": "Next: skillops-reviewer reviews the change against the acceptance criteria.",
    "AWAITING_HUMAN_APPROVAL": "Your decision: reply `APPROVE {id} merge`, `CHANGES {id}: <what to change>` "
                               "or `REJECT {id}`. Nothing is merged until you approve.",
    "CHANGES_REQUESTED": "Next: skillops-coder addresses the feedback.",
    "APPROVED": "Next: skillops-manager merges the approved branch.",
    "COMPLETED": "Merged into main.",
    "REJECTED": "Closed without merging.",
}


def render(record):
    """The reply to post in the room (Mattermost Markdown)."""
    lines = [f"**{record['id']}** · `{record['status']}` · branch `{record.get('branch', '-')}`",
             f"> {record['summary']}"]
    if record.get("evidence"):
        ev = record["evidence"][-1]
        lines.append(f"**Tests:** `{ev['command']}` → exit {ev['exit_code']} ({ev['note']})")
        if ev["changed_files"]:
            lines.append("**Changed files:** " + ", ".join(f"`{f}`" for f in ev["changed_files"]))
        lines.append("```\n" + ev["output_tail"] + "\n```")
    if record.get("review") and record["status"] in ("AWAITING_HUMAN_APPROVAL", "APPROVED", "COMPLETED"):
        lines.append(f"**Review:** {record['review']['verdict']}: {record['review']['notes']}")
    if record.get("feedback") and record["status"] in ("IMPLEMENTING", "CHANGES_REQUESTED"):
        last = record["feedback"][-1]
        lines.append(f"**Feedback from {last['by']}:** {last['text']}")
    if record.get("approval"):
        lines.append(f"**Approved by** {record['approval']['by']} (message `{record['approval']['message_id']}`)")
    if record.get("merge"):
        lines.append(f"**Merge commit:** `{record['merge']['commit']}`")
    lines.append(NEXT.get(record["status"], "").format(id=record["id"]))
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="work")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("reset-demo")
    for name in ("start", "check", "review", "decide", "merge"):
        p = sub.add_parser(name)
        p.add_argument("id")
        if name == "check":
            p.add_argument("--expect", choices=["pass", "fail"], default="pass")
        if name == "review":
            p.add_argument("--verdict", choices=["pass", "changes"], required=True)
            p.add_argument("--notes", required=True)
        if name == "decide":
            p.add_argument("--by", required=True)
            p.add_argument("--message-id", required=True)
    args = parser.parse_args(argv)
    sys.stdin.reconfigure(encoding="utf-8")  # agents send UTF-8; Windows defaults to cp1252
    sys.stdout.reconfigure(encoding="utf-8")
    try:
        if args.cmd == "reset-demo":
            reset_state()
            print(f"Requests cleared; demo repo reset at {reset_demo()}")
            return 0
        if args.cmd == "start":
            record = start(args.id)
        elif args.cmd == "check":
            record = check(args.id, expect=args.expect)
        elif args.cmd == "review":
            record = review(args.id, args.verdict, args.notes)
        elif args.cmd == "decide":
            record = decide(args.id, sys.stdin.read(), args.by, args.message_id)
        else:
            record = merge(args.id)
    except (WorkError, DecisionError, TransitionError, triage.DraftError) as exc:
        print(f"Refused: {exc}", file=sys.stderr)
        return 2
    print(render(record))
    return 0


if __name__ == "__main__":
    sys.exit(main())
