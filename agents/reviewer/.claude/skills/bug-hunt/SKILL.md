---
name: bug-hunt
description: Look for bugs a change missed before giving a SkillOps review verdict. Use during every review, after reading the diff and before `work.py review`.
---

# Hunt for bugs in a change

You cannot run code or edit files: trace inputs through the changed code by reading it. Use only the commands in your CLAUDE.md.

1. **List the changed functions** from `git -C ../../workspace/demo-app diff main...sko-xxxx`.
2. **Trace each input below through each function**, line by line, and write down what it returns or raises:
   - empty string, whitespace only, `None`;
   - one character, a very long value;
   - non-ASCII text (`"Zoë"`, `"李"`), emoji;
   - leading, trailing and repeated separators (`"  Ada   Lovelace "`);
   - for numbers: `0`, negative, the largest valid value.
3. **Find the other callers.** Read the files that import or call each changed function (`git -C ../../workspace/demo-app show main:<file>` shows the original). A fix in one path that leaves a sibling caller broken is a finding.
4. **Match tests to findings.** For each input that matters to the acceptance criteria, there must be a test that covers it. An untested case the criteria cover is a finding.
5. **Verdict.**
   - Any finding: `--verdict changes`, one line per finding with a file reference and the input that breaks it, for example `profile_settings.py:12: initials(" ") raises IndexError`.
   - No finding: `--verdict pass`, and list the inputs you traced in the notes.

Report only what you traced. Do not claim a case passes unless you followed it through the code.
