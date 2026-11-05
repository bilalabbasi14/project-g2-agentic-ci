# CLAUDE.md — rules for Claude Code in this repository

This file is read automatically by Claude Code whenever it runs in this repository. Part A applies to **every** session. Part B describes how to implement an issue. Part C is the detailed procedure for **reviewing pull requests** (used by Ali and Bilal). Part D covers merging.

The full project description is in `docs/PROJECT_CONTEXT.md`. **Read it at the start of every session** before doing anything else. If this file and the context file disagree, stop and ask the user.

---

## Part A — Rules for every session (no exceptions)

1. **Never commit to `main` and never push to `main`.** All work happens on a branch named `p2-<NN>-<short-name>` and reaches `main` only through a pull request. If the current branch is `main` when you are about to commit, stop, tell the user, and create the correct branch first.
2. **Never bypass the pre-push hook** (no `git push --no-verify`, no changing `core.hooksPath`).
3. **Never merge a pull request** unless the user, in this session, explicitly says "merge PR #N". Approving is not merging.
4. **Never force-push, delete branches, close or delete issues, rewrite history, or delete files you did not create**, unless the user explicitly asks in this session. Ask first for anything destructive.
5. **No attribution lines.** Commit messages, PR titles, PR descriptions, review comments and issue comments must not contain `Co-authored-by:` lines, "Generated with …", or any mention of the tool that produced them. Write commit messages as one short imperative summary line, a blank line, and a few lines explaining what and why.
6. **Use the logged-in user's identity only.** Do not change `git config user.name` / `user.email`, and never use a token belonging to someone else.
7. **Never commit secrets or data:** no tokens, keys, `.env`, raw LRTS/DANTE files, source cache, LLM cache, full logs, or `results/**/runs/`. If you see one staged, unstage it and tell the user.
8. **Stay inside the issue's scope.** Change only the files the issue names. If something else needs changing, or the issue is unclear or wrong, do not expand the task: write it in the PR under "Problems found / limitations" and suggest a new issue. A new issue is created only after Ali approves it.
9. **Never edit another member's files** (ownership table in `docs/PROJECT_CONTEXT.md` §9) unless the issue says so.
10. **Leakage rules** (`docs/PROJECT_CONTEXT.md` §6.3) are absolute: no target-build outcomes as model input; tuning only on the `dev` split; never run or inspect test-split results while changing prompts, thresholds or weights.
11. **Every reported number comes from a file under `results/`** produced by a script in the repository. Never type a result by hand into README, docs or code.
12. **Tests never need data or a model.** Use `MockProvider` and the fakes in `tests/fakes.py`. Run `python -m pytest` before every push.
13. **The research paper is out of scope.** Do not write, rewrite or paraphrase paper text. If asked, explain that the course requires the paper to be written by the members themselves.

---

## Part B — Implementing an issue (for whoever is assigned)

1. Find the issue: `gh issue list --assignee @me --state open`. Choose the lowest-numbered issue whose "Depends on" issues are all closed (`gh issue view <N>` for each dependency). If none is ready, say so and stop.
2. Read the issue body completely, then the sections of `docs/PROJECT_CONTEXT.md` it points to, then the existing files it names.
3. Update and branch:
   ```
   git checkout main
   git pull
   git checkout -b p2-<NN>-<short-name>
   ```
4. Implement exactly what the issue says. Write the tests it lists. Run `python -m pytest` until everything passes.
5. Before pushing: `git fetch origin` and `git rebase origin/main` (resolve conflicts, rerun the tests).
6. Push the branch and open the PR:
   ```
   git push -u origin p2-<NN>-<short-name>
   gh pr create --base main --title "[P2-<NN>] <issue title>" --body-file <filled template>
   ```
   The body is the PR template with every section filled in: `Closes #<issue number>`, what changed, the exact test commands and results, each acceptance criterion ticked **only if it is truly met**, problems found, devlog entry.
7. Tell the user the PR link and stop. Do not merge.

---

## Part C — Reviewing a pull request (Ali or Bilal)

The reviewer must not be the PR's author. Review in this order and do not skip steps.

### C1. Collect the facts

```
gh pr view <PR> --json number,title,author,headRefName,baseRefName,body,files,commits
gh pr checks <PR>
gh pr diff <PR>
```

From the PR body, find the linked issue (`Closes #N`) and read it: `gh issue view <N>`. Its **acceptance criteria and "What to build" are the specification you review against.**

### C2. Blocking checks — any failure means "Request changes"

1. **Correct target:** base branch is `main`; head branch is `p2-<NN>-…` matching the issue number.
2. **CI is green:** `gh pr checks <PR>` shows the `tests` job passed. If it is pending, wait; if it failed, request changes and quote the failing test.
3. **Tests pass locally too:**
   ```
   gh pr checkout <PR>
   python -m pytest
   ```
   Record the summary line (e.g. `92 passed`). Return to `main` afterwards (`git checkout main`).
4. **Every acceptance criterion is truly met.** Go through them one by one. For each, find the code, test or file that proves it. A ticked box without evidence counts as not met.
5. **The specified interfaces are respected:** function names, signatures, file paths, CSV column names, config keys and schema names exactly as in the issue and in `src/contracts/`. Other issues depend on them.
6. **Scope and ownership:** only files named in the issue were changed, or each extra file is justified in the PR body. No changes to another member's files without a reason and the owner's agreement. Shared files (`config.yaml`, `requirements.txt`, `src/contracts/*`) change only in P2-03, or with Ali's agreement.
7. **No leakage:**
   - No `actual_outcome` / `outcome` of the target build is used as input to scoring, prompts, features, shortlist or explanations.
   - Tuning (prompts, thresholds, weights) uses only `split == "dev"`.
   - New prompts pass diff and source text through `anonymise`.
8. **Robustness:** every LLM output is validated against a schema; retries and fallbacks follow `docs/PROJECT_CONTEXT.md` §5.4; fallbacks produce `FallbackRecord`s; nothing crashes a whole run because of one bad answer.
9. **Tests are real:** new behaviour has tests; tests use `MockProvider`/fakes and need no data or model; no assertion in an existing test was weakened or deleted without a clear reason in the PR.
10. **Nothing forbidden is committed:** no data, caches, `runs/` JSONs, full logs, `.env`, tokens, keys. Check with
    `gh pr diff <PR> --name-only` and a search of the diff for `ghp_`, `github_pat_`, `token`, `password`, `api_key`.
11. **Commit hygiene:**
    ```
    gh pr view <PR> --json commits --jq '.commits[] | [.authors[].login, .messageHeadline] | @tsv'
    ```
    - Commits are authored by the PR author (the assigned member).
    - No message contains `Co-authored-by` or "Generated with".
    - Messages are meaningful (not "update", "fix", "wip" alone).
12. **Results PRs** (labels `experiment-run`, or files under `results/`):
    - `run_meta.json` shows the expected run id, split, seed, number of builds, and the agreed `main` SHA.
    - `per_build.csv` has the exact columns from P2-15.
    - Numbers quoted in the PR body match the files.
    - No test-split run was used for tuning.

### C3. Non-blocking observations

Report these as suggestions; they do not prevent approval:
- readability, naming, missing docstrings;
- small duplication;
- performance improvements that are not needed now.

### C4. Write the review

Use exactly this structure, in plain words, for the review body:

```
## Review of PR #<PR> for issue #<N> (P2-<NN>)

**Decision:** Approve | Request changes

**Tests:** CI <passed/failed>; local `python -m pytest` -> <summary line>

**Acceptance criteria**
- [x] <criterion> — evidence: <file/test/output>
- [ ] <criterion> — missing because: <reason>

**Blocking problems** (must be fixed before merge)
1. <file:line> — <what is wrong> — <what to change>

**Suggestions** (optional)
1. ...
```

Post it with:
```
gh pr review <PR> --approve --body-file review.md
gh pr review <PR> --request-changes --body-file review.md
```
(Choose the one that matches the decision.) Approve **only** when there are no blocking problems. Then tell the user the decision and stop. **Do not merge.**

### C5. Re-review

When the author pushes fixes, repeat C1–C4, focusing on the previous blocking problems, and say explicitly which are now resolved.

---

## Part D — Merging (Ali only, on explicit instruction)

Merge only when the user says "merge PR #N" **and** all of the following hold:
- an approving review from someone other than the author;
- CI green on the latest commit;
- the branch is up to date with `main`, or merges without conflicts.

Use a merge commit so each member's individual commits stay in the history:
```
gh pr merge <PR> --merge
```
Do not squash and do not rebase-merge. After merging, `git checkout main && git pull`.

**Check for direct pushes** (run after each merge and before the release). Every commit on `main` after the P2-01 merge should be a merge commit created by a PR:
```
git log origin/main --first-parent --oneline
```
Anything after the P2-01 merge that is not "Merge pull request #…" was pushed directly. Report it to the user; do not try to undo it yourself.
