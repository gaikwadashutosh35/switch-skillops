---
name: debug
description: Root-cause debugging for a SkillOps request. Use when the cause of a bug is not obvious, when a regression test will not fail the way you expect, or when a fix did not make `work.py check` pass.
---

# Debug a request

Find the cause before you change code. Use only the commands in your CLAUDE.md; this skill adds no new ones.

1. **Reproduce.** Write the regression test from the request's steps, then run `python ../../skillops/work.py check SKO-xxxx --expect fail`. Read the traceback bottom-up: the last frame inside `../../workspace/demo-app` is where to start. If the test passes, it does not reproduce the bug yet: make it closer to the request's steps before going on.
2. **Read the failing code.** Open the file and function from that frame, and the inputs that reach it. Say in the room, in one line, what the code does with the request's input.
3. **One hypothesis at a time.** State it: "`initials('')` fails because `split(' ')` returns `['']` and `[0][0]` indexes an empty string." The failing test must fail for exactly that reason; if the error differs, the hypothesis is wrong.
4. **Find every caller.** Search `../../workspace/demo-app` for the function's name. Fix where all callers pass through, not only the path the request names.
5. **Smallest fix at the root.** Change only that function. Do not reformat or rename nearby code.
6. **Check the neighbours.** Other inputs that reach the same line (empty, whitespace only, `None`, one character, unicode) must not still fail. Add a test for any that the request's acceptance criteria cover.
7. **Report.** Run step 7 of your CLAUDE.md, and post the cause in one sentence with a file reference, for example `profile_settings.py:12`.

If three hypotheses in a row are wrong, stop and post what you tried and what you saw. Do not guess a fix.
