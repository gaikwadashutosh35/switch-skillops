import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from skillops import triage, work

FIX = '''
def initials(display_name):
    """Initials shown in the avatar, e.g. "Ada Lovelace" -> "AL"."""
    return "".join(part[0].upper() for part in display_name.split())
'''

REGRESSION_TEST = '''
import unittest
from profile_settings import save_profile


class EmptyNameTest(unittest.TestCase):
    def test_empty_display_name_saves(self):
        self.assertEqual(save_profile({}, "u1", "a@b.c", "")["initials"], "")
'''


class WorkTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        tmp = Path(self._tmp.name)
        self.state = tmp / "state"
        self.repo = tmp / "workspace" / "demo-app"
        work.reset_demo(self.repo)
        draft = {
            "request_text": "Settings page crashes when I save an empty display name.",
            "summary": "Settings page crashes on empty display name",
            "type": "bug",
            "steps_to_reproduce": ["Open settings", "Clear display name", "Save"],
            "acceptance_criteria": ["Saving with an empty display name succeeds"],
        }
        self.id = triage.submit(json.dumps(draft), self.state)["id"]

    def tearDown(self):
        self._tmp.cleanup()

    def call(self, fn, *args, **kwargs):
        return fn(self.id, *args, repo=self.repo, state_dir=self.state, **kwargs)

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.repo), *args], capture_output=True,
                              text=True, check=True).stdout.strip()

    def write(self, name, text):
        (self.repo / name).write_text(text, encoding="utf-8")

    def append_fix(self):
        source = (self.repo / "profile_settings.py").read_text(encoding="utf-8")
        start = source.index("def initials")
        end = source.index("def save_profile")
        self.write("profile_settings.py", source[:start] + FIX.strip() + "\n\n\n" + source[end:])

    def commit(self, message):
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)

    def to_qa(self):
        self.call(work.start)
        self.write("test_regression.py", REGRESSION_TEST)
        self.call(work.check, expect="fail")
        self.append_fix()
        self.commit("Fix initials for empty display name")
        return self.call(work.check)

    def to_approval(self):
        self.to_qa()
        return self.call(work.review, verdict="pass", notes="Matches the acceptance criteria.")

    # Demo reset

    def test_reset_demo_creates_a_clean_repo_on_main(self):
        self.assertEqual(self.git("branch", "--show-current"), "main")
        self.assertEqual(self.git("status", "--porcelain"), "")
        work.reset_demo(self.repo)
        self.assertEqual(self.git("log", "--oneline").count("\n"), 0)

    def test_running_checks_leaves_the_working_tree_clean(self):
        # The agents' shells write bytecode; make sure this test does too.
        with mock.patch.dict(os.environ):
            os.environ.pop("PYTHONDONTWRITEBYTECODE", None)
            self.call(work.start)
            self.call(work.check, expect="fail")
        self.assertEqual(self.git("status", "--porcelain"), "")

    def test_reset_state_removes_only_request_records(self):
        keep = self.state / "notes.txt"
        keep.write_text("keep me", encoding="utf-8")
        work.reset_state(self.state)
        self.assertEqual(list(self.state.glob("SKO-*.json")), [])
        self.assertTrue(keep.exists())

    def test_reset_demo_refuses_paths_outside_a_workspace_dir(self):
        with self.assertRaises(work.WorkError):
            work.reset_demo(self.repo.parent.parent / "elsewhere")

    # Start

    def test_start_plans_and_creates_branch(self):
        r = self.call(work.start)
        self.assertEqual(r["status"], "PLANNED")
        self.assertEqual(r["branch"], "sko-0001")
        self.assertEqual(self.git("branch", "--show-current"), "sko-0001")

    def test_start_refuses_request_that_needs_clarification(self):
        unclear = triage.submit(json.dumps({"request_text": "x", "summary": "x", "type": "feature"}),
                                self.state)
        with self.assertRaises(triage.TransitionError):
            work.start(unclear["id"], repo=self.repo, state_dir=self.state)

    # Check

    def test_failing_check_records_reproduction_and_stays_implementing(self):
        self.call(work.start)
        self.write("test_regression.py", REGRESSION_TEST)
        r = self.call(work.check, expect="fail")
        self.assertEqual(r["status"], "IMPLEMENTING")
        ev = r["evidence"][-1]
        self.assertNotEqual(ev["exit_code"], 0)
        self.assertIn("IndexError", ev["output_tail"])
        self.assertEqual(ev["expect"], "fail")

    def test_passing_check_with_uncommitted_changes_stays_implementing(self):
        self.call(work.start)
        self.append_fix()
        r = self.call(work.check)
        self.assertEqual(r["status"], "IMPLEMENTING")
        self.assertIn("commit", r["evidence"][-1]["note"])

    def test_passing_committed_check_moves_to_qa_with_changed_files(self):
        r = self.to_qa()
        self.assertEqual(r["status"], "QA_REVIEW")
        self.assertEqual(r["evidence"][-1]["exit_code"], 0)
        self.assertIn("profile_settings.py", r["evidence"][-1]["changed_files"])

    def test_check_with_failing_tests_never_reaches_qa(self):
        self.call(work.start)
        self.write("test_regression.py", REGRESSION_TEST)
        self.commit("Add failing regression test")
        r = self.call(work.check)
        self.assertEqual(r["status"], "IMPLEMENTING")

    def test_secrets_are_redacted_from_evidence(self):
        self.call(work.start)
        self.write("test_leak.py", "import unittest\nclass T(unittest.TestCase):\n"
                   "    def test_x(self):\n        self.fail('token=abc123secretvalue')\n")
        r = self.call(work.check, expect="fail")
        self.assertNotIn("abc123secretvalue", r["evidence"][-1]["output_tail"])

    # Review

    def test_review_pass_awaits_human_approval(self):
        r = self.to_approval()
        self.assertEqual(r["status"], "AWAITING_HUMAN_APPROVAL")
        self.assertEqual(r["review"]["verdict"], "pass")

    def test_review_changes_returns_to_implementing_with_feedback(self):
        self.to_qa()
        r = self.call(work.review, verdict="changes", notes="Add a test for whitespace-only names.")
        self.assertEqual(r["status"], "IMPLEMENTING")
        self.assertIn("whitespace", r["feedback"][-1]["text"])

    def test_review_outside_qa_is_refused(self):
        self.call(work.start)
        with self.assertRaises(triage.TransitionError):
            self.call(work.review, verdict="pass", notes="ok")

    def test_review_refuses_when_the_repo_is_not_on_the_request_branch(self):
        # e.g. a second request was started, which checks out its own branch
        self.to_qa()
        self.git("checkout", "-q", "main")
        with self.assertRaises(work.WorkError):
            self.call(work.review, verdict="pass", notes="ok")
        self.assertEqual(triage.load(self.id, self.state)["status"], "QA_REVIEW")

    def test_review_refuses_uncommitted_changes(self):
        self.to_qa()
        self.write("extra.py", "x = 1\n")
        with self.assertRaises(work.WorkError):
            self.call(work.review, verdict="pass", notes="ok")

    def test_review_records_the_commit_it_tested(self):
        r = self.to_approval()
        self.assertEqual(r["review"]["commit"], self.git("rev-parse", "HEAD"))

    # Human decision

    def test_vague_or_wrong_approvals_are_refused(self):
        self.to_approval()
        for message in ["looks good", "approve", "APPROVE SKO-0002 merge", "APPROVE SKO-0001 deploy",
                        "yes merge it"]:
            with self.subTest(message=message):
                with self.assertRaises(work.DecisionError):
                    self.call(work.decide, message, by="user", message_id="m1")

    def test_agents_cannot_approve(self):
        self.to_approval()
        with self.assertRaises(work.DecisionError):
            self.call(work.decide, "APPROVE SKO-0001 merge", by="skillops-coder", message_id="m1")

    def test_approval_before_review_is_refused(self):
        self.call(work.start)
        with self.assertRaises(work.DecisionError):
            self.call(work.decide, "APPROVE SKO-0001 merge", by="user", message_id="m1")

    def test_exact_approval_with_mention_is_accepted(self):
        self.to_approval()
        r = self.call(work.decide, "@skillops-manager APPROVE SKO-0001 merge", by="user", message_id="m9")
        self.assertEqual(r["status"], "APPROVED")
        self.assertEqual(r["approval"]["by"], "user")
        self.assertEqual(r["approval"]["message_id"], "m9")

    def test_changes_request_keeps_feedback_and_reopens_work(self):
        self.to_approval()
        r = self.call(work.decide, "CHANGES SKO-0001: also handle names with two spaces",
                      by="user", message_id="m2")
        self.assertEqual(r["status"], "CHANGES_REQUESTED")
        self.assertIn("two spaces", r["feedback"][-1]["text"])
        r = self.call(work.check)
        self.assertEqual(r["status"], "QA_REVIEW")

    def test_reject_closes_the_request(self):
        self.to_approval()
        r = self.call(work.decide, "REJECT SKO-0001", by="user", message_id="m3")
        self.assertEqual(r["status"], "REJECTED")

    # Merge

    def test_merge_without_approval_is_refused(self):
        self.to_approval()
        with self.assertRaises(work.WorkError):
            self.call(work.merge)
        self.assertNotIn("Fix initials", self.git("log", "main", "--oneline"))

    def test_merge_after_approval_completes(self):
        self.to_approval()
        self.call(work.decide, "APPROVE SKO-0001 merge", by="user", message_id="m4")
        r = self.call(work.merge)
        self.assertEqual(r["status"], "COMPLETED")
        self.assertIn("Fix initials", self.git("log", "main", "--oneline"))
        self.assertEqual(self.git("branch", "--show-current"), "main")

    def test_merge_takes_only_the_reviewed_commit(self):
        self.to_approval()
        self.write("unreviewed.py", "x = 1\n")
        self.commit("Unreviewed change after review")
        self.call(work.decide, "APPROVE SKO-0001 merge", by="user", message_id="m5")
        r = self.call(work.merge)
        self.assertEqual(r["status"], "COMPLETED")
        log = self.git("log", "main", "--oneline")
        self.assertIn("Fix initials", log)
        self.assertNotIn("Unreviewed change", log)

    def test_decide_reads_the_message_as_utf8(self):
        # Windows' default stdin encoding is cp1252; the agents send UTF-8.
        seen = []
        stdin = io.TextIOWrapper(io.BytesIO("CHANGES SKO-0001: Zoë 李 😀".encode("utf-8")), encoding="cp1252")
        with mock.patch.object(work, "decide", side_effect=lambda i, m, *a: seen.append(m) or self.fail_decide()), \
                mock.patch.object(sys, "stdin", stdin), mock.patch.object(sys, "stderr", io.StringIO()):
            work.main(["decide", "SKO-0001", "--by", "user", "--message-id", "m6"])
        self.assertEqual(seen, ["CHANGES SKO-0001: Zoë 李 😀"])

    @staticmethod
    def fail_decide():
        raise work.DecisionError("stop here")

    def test_redaction_covers_common_secret_formats(self):
        secret = "S3cretValue_42"
        for text in [f"token: {secret}", f"TOKEN={secret}", f'"token": "{secret}"', f"{{'password': '{secret}'}}",
                     f"Authorization: Bearer {secret}", f"password = {secret}", f"api_key={secret}",
                     f"API-KEY: {secret}", f"MY_TOKEN={secret}", f"GITHUB_TOKEN={secret}",
                     f"secret_key='{secret}'", f"passwd={secret}", f"ghp_{secret}", f"AKIA{secret.upper()}",
                     f"postgres://admin:{secret}@db/app", f"--password {secret}", f"x-api-key: {secret}",
                     f"client_secret={secret}"]:
            with self.subTest(text=text):
                self.assertNotIn(secret.lower(), work.redact(text).lower())

    def test_redaction_keeps_ordinary_test_output(self):
        text = "FAIL: test_password_reset (test_auth.AuthTest.test_password_reset)\nAssertionError: 'token' != 'x'"
        self.assertEqual(work.redact(text), text)

    def test_render_shows_status_and_last_evidence(self):
        text = work.render(self.to_qa())
        for part in ("SKO-0001", "QA_REVIEW", "exit 0", "profile_settings.py"):
            self.assertIn(part, text)


if __name__ == "__main__":
    unittest.main()
