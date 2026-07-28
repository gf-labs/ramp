---
topic: git
node_count: 27
version: 1
source_url: https://git-scm.com/book/en/v2
goal: ramp them up on Git as a version-control tool — how to branch and merge, collaborate through remotes and pull requests, rewrite and recover history safely, and reason about the object model with confidence
description: Git version control — from the snapshot mental model through branching, remotes, history rewriting and recovery, advanced tooling, and internals. Grounded in the Pro Git book.
---

# Git Knowledge Graph Schema

This file defines the curriculum for the `git` topic. It follows the Pro Git book (git-scm.com/book/en/v2): the mental model and everyday recording in *Git Basics*, *Git Branching*, distributed collaboration, the *Git Tools* recovery and power features, and *Git Internals*. Scoped to using Git as a version-control tool — hosting-platform workflows (GitHub/GitLab pull requests), server administration and server-side hooks, submodules, and Git LFS are out of scope. 27 nodes across 6 branches, foundations-first with each branch unlocking the next.

---

## Node definitions

27 nodes across 6 branches.

### [ROOT] Git foundations (always unlocked — 5 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|-----------|-----|
| What Git is: snapshots, not diffs | Can explain that Git stores full-tree snapshots content-addressed by SHA (not per-file deltas), and can contrast this with delta/diff-based version control | Qualitative | None | https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F | git-what-git-is-snapshots-not-diffs |
| Repository setup: init and clone | Has created a repository with `git init` and/or cloned one; knows what lives in `.git/` and how `init` differs from `clone` | Historical / Exercise | git history exists → `[✓\|historical]`; `.gitignore` present → `[~\|artifact]` | https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository | git-repository-setup-init-and-clone |
| The three states: working tree, index, commit | Can explain the working tree, staging area (index), and committed history, and how `add`/`commit` move changes between them — and what staging is *for* | Qualitative | None | https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F | git-the-three-states-working-tree-index-commit |
| Recording changes: add, commit, status, diff | Has staged and committed changes; reads `git status`, distinguishes `git diff` (unstaged) from `git diff --staged`, and writes meaningful commit messages | Exercise / Historical | git history exists → `[~\|historical]` | https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository | git-recording-changes-add-commit-status-diff |
| Viewing history with log | Navigates history with `git log` and its key flags (`--oneline`, `--graph`, `-p`, `--stat`); can find *when and why* a change was made | Exercise / Qualitative | git history exists → `[~\|historical]` | https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History | git-viewing-history-with-log |

### [A] Branching and merging (5 nodes, unlocks when ROOT ≥ 3 `[✓]`)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|-----------|-----|
| Branches as movable pointers (and HEAD) | Can explain that a branch is a lightweight movable pointer to a commit and what HEAD refers to; creates and switches branches with `git switch` / `git branch` | Qualitative / Exercise | None | https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell | git-branches-as-movable-pointers-and-head |
| Basic branch-and-merge workflow | Has created a topic branch, committed on it, and merged it back; understands the everyday topic-branch loop | Exercise / Historical | merge commits in history → `[~\|historical]` | https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging | git-basic-branch-and-merge-workflow |
| Fast-forward vs. merge commits | Can explain when a merge fast-forwards versus creates a merge commit, and why the distinction matters for history | Qualitative | None | https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging | git-fast-forward-vs-merge-commits |
| Resolving merge conflicts | Has resolved a merge conflict — reads the conflict markers, edits, stages, and completes the merge (or aborts with `--abort`); can explain what a conflict represents | Exercise / Qualitative | None | https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging | git-resolving-merge-conflicts |
| Branch management and workflows | Lists, deletes, and renames branches; can describe a branching workflow (topic branches, long-running branches) used in practice | Qualitative / Historical | None | https://git-scm.com/book/en/v2/Git-Branching-Branch-Management | git-branch-management-and-workflows |

### [B] Remotes and collaboration (4 nodes, unlocks when Branch A ≥ 3 `[✓]`)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|-----------|-----|
| Remotes: fetch, pull, push | Can explain the difference between `fetch`, `pull`, and `push`, and has synchronized a local repository with a remote | Exercise / Historical | None | https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes | git-remotes-fetch-pull-push |
| Remote-tracking branches | Can explain what `origin/main` is, how upstream tracking works, and how local branches relate to remote-tracking refs | Qualitative | None | https://git-scm.com/book/en/v2/Git-Branching-Remote-Branches | git-remote-tracking-branches |
| Collaboration: pull requests and shared branches | Has contributed through a pull-request or shared-branch workflow; understands review and integration into a shared branch | Historical / Qualitative | conventional-commit prefixes in history → `[~\|historical]` | https://git-scm.com/book/en/v2/Distributed-Git-Contributing-to-a-Project | git-collaboration-pull-requests-and-shared-branches |
| Rebase vs. merge for integration | Can articulate the tradeoff — rebase for linear history versus merge for preserved topology — and state the golden rule: never rebase commits that have been pushed to a shared branch | Qualitative | None | https://git-scm.com/book/en/v2/Git-Branching-Rebasing | git-rebase-vs-merge-for-integration |

### [C] Rewriting and recovery (5 nodes, unlocks when Branch B ≥ 2 `[✓]`)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|-----------|-----|
| reset: --soft, --mixed, --hard | Can explain what each reset mode does to HEAD, the index, and the working tree, and choose the right one to undo work safely | Qualitative | None | https://git-scm.com/book/en/v2/Git-Tools-Reset-Demystified | git-reset-soft-mixed-hard |
| revert vs. reset | Can explain when to use `revert` (undo public history with a new commit) versus `reset` (move a local ref), and why revert is safe on shared branches | Qualitative / Historical | revert commits in history → `[~\|historical]` | https://git-scm.com/book/en/v2/Git-Basics-Undoing-Things | git-revert-vs-reset |
| Interactive rebase: squash, reword, reorder | Has used `git rebase -i` to clean up history (squash, fixup, reword, reorder) and can explain when doing so is safe | Exercise / Historical | None | https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History | git-interactive-rebase-squash-reword-reorder |
| The reflog and recovering lost work | Uses `git reflog` to recover a "lost" commit after a bad reset or rebase, and treats the reflog as Git's safety net | Exercise / Qualitative | None | https://git-scm.com/book/en/v2/Git-Internals-Maintenance-and-Data-Recovery | git-the-reflog-and-recovering-lost-work |
| cherry-pick | Applies a specific commit onto another branch with `git cherry-pick` and can explain a concrete use case | Exercise / Qualitative | None | https://git-scm.com/book/en/v2/Distributed-Git-Maintaining-a-Project | git-cherry-pick |

### [D] Advanced tooling (5 nodes, unlocks when Branch C ≥ 2 `[✓]`)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|-----------|-----|
| Stashing work in progress | Has used `git stash` to shelve and restore uncommitted work, and knows the difference between `stash pop` and `stash apply` | Exercise / Historical | None | https://git-scm.com/book/en/v2/Git-Tools-Stashing-and-Cleaning | git-stashing-work-in-progress |
| Worktrees for parallel work | Has used `git worktree` to check out multiple branches simultaneously, and can explain when it beats stashing or a second clone | Exercise / Historical | worktrees in use → `[~\|artifact]` | https://git-scm.com/docs/git-worktree | git-worktrees-for-parallel-work |
| Bisect to find a regression | Uses `git bisect` (or can explain its binary-search model) to locate the commit that introduced a bug | Qualitative / Exercise | None | https://git-scm.com/book/en/v2/Git-Tools-Debugging-with-Git | git-bisect-to-find-a-regression |
| Tags and annotated releases | Creates annotated tags to mark releases and can explain lightweight versus annotated tags | Artifact / Exercise | tags present → `[~\|artifact]` | https://git-scm.com/book/en/v2/Git-Basics-Tagging | git-tags-and-annotated-releases |
| Client-side hooks | Knows what client-side hooks are (e.g. `pre-commit`, `commit-msg`) and has wired up or used one | Artifact / Qualitative | None | https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks | git-client-side-hooks |

### [E] Internals (3 nodes, unlocks when Branch D ≥ 2 `[✓]`)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|-----------|-----|
| Git objects: blobs, trees, commits | Can explain Git's content-addressed object model — blobs (file content), trees (directory snapshots), and commits (a tree plus parents and metadata) | Qualitative | None | https://git-scm.com/book/en/v2/Git-Internals-Git-Objects | git-git-objects-blobs-trees-commits |
| Refs and HEAD | Can explain refs as named pointers to commits, and how branches, tags, and HEAD are all refs — tying back to the branching model | Qualitative | None | https://git-scm.com/book/en/v2/Git-Internals-Git-References | git-refs-and-head |
| The commit DAG; plumbing vs. porcelain | Can explain commit ancestry as a directed acyclic graph (parents), and the plumbing-versus-porcelain split — connecting internals to everyday commands | Qualitative | None | https://git-scm.com/book/en/v2/Git-Internals-Plumbing-and-Porcelain | git-the-commit-dag-plumbing-vs-porcelain |

---

## Probes

| name | primitive | args |
|------|-----------|------|
| git_history          | git-log-grep       | . |
| gitignore            | file-exists        | .gitignore |
| merge_commits        | git-log-grep       | ^Merge |
| conventional_commits | git-log-grep       | ^(feat\|fix\|refactor\|chore\|docs) |
| revert_commits       | git-log-grep       | ^Revert |
| worktrees            | git-worktree-count | — |
| tags                 | glob-count         | .git/refs/tags/* |

Notes: `git_history` counts commits (any message), so it is > 0 in any repo with history. `worktrees` counts `git worktree list` lines, which is always ≥ 1 because the main worktree is listed — so the signal below thresholds at **> 1** (a *linked* worktree beyond main). Even then, a linked worktree is not proof the *user* ran `git worktree` — agent tooling (e.g. Claude Code's worktree isolation) creates them too — so it seeds `[~]`, never `[✓]` (the direct-witness rule). `tags` counts loose tag refs; tags packed into `.git/packed-refs` are not seen, so it is a best-effort seed, never a false positive.

---

## Detection signals

| Collected evidence | Node → status |
|--------------------|---------------|
| git_history > 0 | ROOT: "Repository setup: init and clone" → `[✓\|historical]` |
| git_history > 0 | ROOT: "Recording changes: add, commit, status, diff" → `[~\|historical]` |
| git_history > 0 | ROOT: "Viewing history with log" → `[~\|historical]` |
| gitignore exists | ROOT: "Repository setup: init and clone" → `[~\|artifact]` |
| merge_commits > 0 | A: "Basic branch-and-merge workflow" → `[~\|historical]` |
| conventional_commits > 0 | B: "Collaboration: pull requests and shared branches" → `[~\|historical]` |
| revert_commits > 0 | C: "revert vs. reset" → `[~\|historical]` |
| worktrees > 1 (a linked worktree beyond the always-present main) | D: "Worktrees for parallel work" → `[~\|artifact]` |
| tags > 0 (loose tag refs present) | D: "Tags and annotated releases" → `[~\|artifact]` |

---

## Gap questions

| Branch | Gap | Ask this |
|--------|-----|----------|
| [ROOT] | Snapshot model | "Explain how Git stores your project's history — does it save the differences between versions, or something else? Why does that design choice matter?" |
| [ROOT] | Repository setup | "You're starting a brand-new project versus joining an existing one — which command sets up Git for each, and what actually lands in the `.git/` directory when it does?" |
| [ROOT] | Three states | "Walk me through what happens to a file as it goes from edited to committed. What are the three areas it passes through, and what is the staging area *for*?" |
| [ROOT] | Recording changes | "You've edited three files but want to commit only one. Walk me through the exact commands, and how you'd check what's staged versus not." |
| [ROOT] | Viewing history | "How do you find the commit that introduced a specific change? Which `git log` flags do you reach for?" |
| [A] | Branch model | "When you create a branch, is Git copying your files? Explain what a branch and HEAD actually are." |
| [A] | Branch-and-merge | "Walk me through your last feature-branch-to-merge cycle — what commands, and what did the history look like after?" |
| [A] | Fast-forward vs. merge | "Sometimes a merge makes a merge commit and sometimes it doesn't. Explain when each happens and why it matters." |
| [A] | Conflicts | "You run a merge and hit a conflict. Walk me through exactly what you do — what the markers mean, and how you finish or back out." |
| [A] | Workflows | "Describe the branching workflow you or your team use — how branches get created, integrated, and cleaned up." |
| [B] | fetch vs. pull | "Explain the difference between fetch and pull. When would you deliberately fetch *without* pulling?" |
| [B] | Remote-tracking | "What is `origin/main`, exactly? How does it relate to your local `main`, and what does 'tracking' mean?" |
| [B] | Collaboration | "Walk me through how you get a change reviewed and merged on a shared project — from local commit to merged." |
| [B] | Rebase vs. merge | "When do you rebase versus merge, and what is the one rule you never break with rebase? Why is breaking it dangerous?" |
| [C] | reset modes | "Explain the difference between `reset --soft`, `--mixed`, and `--hard`. Give a scenario where picking the wrong one loses work." |
| [C] | revert vs. reset | "You need to undo a commit that's already been pushed and pulled by teammates — reset or revert? Why?" |
| [C] | Interactive rebase | "You have five messy WIP commits before opening a PR. How do you clean them into a tidy history, and when is that unsafe?" |
| [C] | reflog recovery | "You ran a hard reset and lost a commit you needed. How do you get it back, and what makes that recovery possible?" |
| [C] | cherry-pick | "You need one specific commit from another branch, not the whole branch. What command, and when is this the right tool?" |
| [D] | stash | "You're mid-change and must switch branches urgently. How do you set work aside and restore it, and what's `pop` vs. `apply`?" |
| [D] | worktrees | "How would you work on two branches at once without stashing or re-cloning? What does `git worktree` give you?" |
| [D] | bisect | "A bug appeared somewhere in the last 200 commits. How do you find the exact commit efficiently?" |
| [D] | tags | "How do you mark a release in Git, and what's the difference between a lightweight and an annotated tag?" |
| [D] | hooks | "What's a client-side hook? Give an example of one you'd use and what it would enforce." |
| [E] | Object model | "Explain Git's object model — what are blobs, trees, and commits, and how are they named?" |
| [E] | Refs | "What is a ref? How are branches, tags, and HEAD all the same underlying thing?" |
| [E] | DAG / plumbing | "Explain how commits form a graph. What's the difference between 'plumbing' and 'porcelain' commands?" |

### Qualitative rubric

- **`[✓]` Demonstrated**: Contains at least one specific, verifiable detail — the actual command/flag, an observed behavior, a tradeoff navigated, or a causal explanation of *why*, not just *what*.
- **`[~]` Self-reported**: Affirmative but vague. "Yeah, I branch and merge" with no mechanism or scenario.
- **`[ ]` Not yet**: Negative, "not sure," or "heard of it but haven't done it."

### Answer → node mapping

| Answer contains | Node → status |
|-----------------|---------------|
| Snapshots / content-addressed / SHA, contrasted with diffs | ROOT: "What Git is: snapshots, not diffs" → `[✓\|reported]` |
| init vs. clone distinguished + what lives in `.git/` | ROOT: "Repository setup: init and clone" → `[✓\|reported]` |
| Working tree / staging (index) / commit named, with what staging is for | ROOT: "The three states" → `[✓\|reported]` |
| Specific `add`/`status`/`diff --staged` usage to stage selectively | ROOT: "Recording changes" → `[✓\|reported]` |
| Specific log flags (`--oneline`/`--graph`/`-p`/`-S`) to locate a change | ROOT: "Viewing history with log" → `[✓\|reported]` |
| Branch = movable pointer, HEAD explained, no file copy | A: "Branches as movable pointers (and HEAD)" → `[✓\|reported]` |
| Concrete feature-branch → merge cycle with commands | A: "Basic branch-and-merge workflow" → `[✓\|reported]` |
| When fast-forward happens vs. a merge commit, and why | A: "Fast-forward vs. merge commits" → `[✓\|reported]` |
| Conflict markers explained + stage-and-continue or `--abort` | A: "Resolving merge conflicts" → `[✓\|reported]` |
| A real branching workflow with lifecycle detail | A: "Branch management and workflows" → `[✓\|reported]` |
| fetch-vs-pull distinction with a fetch-only scenario | B: "Remotes: fetch, pull, push" → `[✓\|reported]` |
| `origin/main` as remote-tracking ref + upstream tracking | B: "Remote-tracking branches" → `[✓\|reported]` |
| Concrete review-to-merge flow (PR or shared branch) | B: "Collaboration: pull requests and shared branches" → `[✓\|reported]` |
| Rebase/merge tradeoff + the never-rebase-public rule with reason | B: "Rebase vs. merge for integration" → `[✓\|reported]` |
| The three reset modes distinguished + a data-loss scenario | C: "reset: --soft, --mixed, --hard" → `[✓\|reported]` |
| revert-for-public vs. reset-for-local with reason | C: "revert vs. reset" → `[✓\|reported]` |
| Concrete `rebase -i` cleanup (squash/reword) + safety caveat | C: "Interactive rebase: squash, reword, reorder" → `[✓\|reported]` |
| reflog used to recover a lost commit + why it works | C: "The reflog and recovering lost work" → `[✓\|reported]` |
| `cherry-pick` of a specific commit + a real use case | C: "cherry-pick" → `[✓\|reported]` |
| `stash` shelve/restore + `pop` vs. `apply` distinction | D: "Stashing work in progress" → `[✓\|reported]` |
| `git worktree` for parallel checkouts + when it beats stashing | D: "Worktrees for parallel work" → `[✓\|reported]` |
| `bisect` binary-search to find the offending commit | D: "Bisect to find a regression" → `[✓\|reported]` |
| Annotated vs. lightweight tags + marking a release | D: "Tags and annotated releases" → `[✓\|reported]` |
| A specific client-side hook and what it enforces | D: "Client-side hooks" → `[✓\|reported]` |
| Blobs/trees/commits explained + content addressing | E: "Git objects: blobs, trees, commits" → `[✓\|reported]` |
| Refs as pointers; branches/tags/HEAD as refs | E: "Refs and HEAD" → `[✓\|reported]` |
| Commit ancestry as a DAG + plumbing/porcelain split | E: "The commit DAG; plumbing vs. porcelain" → `[✓\|reported]` |

---

## Unlock thresholds

- Branch A unlocks when ROOT ≥ 3 `[✓]`
- Branch B unlocks when Branch A ≥ 3 `[✓]`
- Branch C unlocks when Branch B ≥ 2 `[✓]`
- Branch D unlocks when Branch C ≥ 2 `[✓]`
- Branch E unlocks when Branch D ≥ 2 `[✓]`

Both `[✓]` and `[~]` count toward unlock thresholds.

---

## Tier definitions

| Tier | Criterion |
|------|-----------|
| Explorer | ROOT incomplete |
| Builder | ROOT complete, Branch A/B in progress |
| Practitioner | Branch C/D active |
| Expert | All branches complete |

---

## Tree render template

```
Git Foundations
    [?] What Git is: snapshots, not diffs
    [?] Repository setup: init and clone
    [?] The three states: working tree, index, commit
    [?] Recording changes: add, commit, status, diff
    [?] Viewing history with log

Branching and Merging   [if locked: "(unlock: complete 3 Git Foundations)"]
    [?] Branches as movable pointers (and HEAD)
    [?] Basic branch-and-merge workflow
    [?] Fast-forward vs. merge commits
    [?] Resolving merge conflicts
    [?] Branch management and workflows

Remotes and Collaboration   [if locked: "(unlock: complete 3 Branching and Merging skills)"]
    [?] Remotes: fetch, pull, push
    [?] Remote-tracking branches
    [?] Collaboration: pull requests and shared branches
    [?] Rebase vs. merge for integration

Rewriting and Recovery   [if locked: "(unlock: complete 2 Remotes and Collaboration skills)"]
    [?] reset: --soft, --mixed, --hard
    [?] revert vs. reset
    [?] Interactive rebase: squash, reword, reorder
    [?] The reflog and recovering lost work
    [?] cherry-pick

Advanced Tooling   [if locked: "(unlock: complete 2 Rewriting and Recovery skills)"]
    [?] Stashing work in progress
    [?] Worktrees for parallel work
    [?] Bisect to find a regression
    [?] Tags and annotated releases
    [?] Client-side hooks

Internals   [if locked: "(unlock: complete 2 Advanced Tooling skills)"]
    [?] Git objects: blobs, trees, commits
    [?] Refs and HEAD
    [?] The commit DAG; plumbing vs. porcelain
```

---

## Saved tree file template

```markdown
---
version: 3
topic: git
user: [git config user.name or "unknown"]
email: [git config user.email or "unknown"]
updated: [today's date YYYY-MM-DD]
level: [Explorer / Builder / Practitioner / Expert]
xp: [CURRENT_XP]
---

# Git Knowledge Graph

*[✓] Demonstrated · [~] Self-reported · [ ] Not yet · [★] Mastery target · [·] Locked*

## [ROOT] Git Foundations
- [STATUS|TYPE] What Git is: snapshots, not diffs
- [STATUS|TYPE] Repository setup: init and clone
- [STATUS|TYPE] The three states: working tree, index, commit
- [STATUS|TYPE] Recording changes: add, commit, status, diff
- [STATUS|TYPE] Viewing history with log

## [A] Branching and Merging
- [STATUS|TYPE] Branches as movable pointers (and HEAD)
- [STATUS|TYPE] Basic branch-and-merge workflow
- [STATUS|TYPE] Fast-forward vs. merge commits
- [STATUS|TYPE] Resolving merge conflicts
- [STATUS|TYPE] Branch management and workflows

## [B] Remotes and Collaboration
- [STATUS|TYPE] Remotes: fetch, pull, push
- [STATUS|TYPE] Remote-tracking branches
- [STATUS|TYPE] Collaboration: pull requests and shared branches
- [STATUS|TYPE] Rebase vs. merge for integration

## [C] Rewriting and Recovery
- [STATUS|TYPE] reset: --soft, --mixed, --hard
- [STATUS|TYPE] revert vs. reset
- [STATUS|TYPE] Interactive rebase: squash, reword, reorder
- [STATUS|TYPE] The reflog and recovering lost work
- [STATUS|TYPE] cherry-pick

## [D] Advanced Tooling
- [STATUS|TYPE] Stashing work in progress
- [STATUS|TYPE] Worktrees for parallel work
- [STATUS|TYPE] Bisect to find a regression
- [STATUS|TYPE] Tags and annotated releases
- [STATUS|TYPE] Client-side hooks

## [E] Internals
- [STATUS|TYPE] Git objects: blobs, trees, commits
- [STATUS|TYPE] Refs and HEAD
- [STATUS|TYPE] The commit DAG; plumbing vs. porcelain

## Frontier
- [frontier node name] — [criterion one-liner]

## Notes
<!-- Add personal notes here -->
```
