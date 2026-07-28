---
topic: bash
node_count: 29
version: 1
source_url: https://www.gnu.org/software/bash/manual/
goal: ramp them up on Bash as a scripting and automation tool — write scripts that run and read cleanly, reason about quoting and the expansions that cause the most bugs, make scripts robust with strict mode and traps, and understand the shell's execution and expansion model
description: Bash scripting — from the shell-and-language mental model through control flow, functions, robustness (strict mode, quoting, traps, ShellCheck), redirection and pipelines, and the expansion machinery. Grounded in the GNU Bash Reference Manual.
---

# Bash Knowledge Graph Schema

This file defines the curriculum for the `bash` topic. It follows the GNU Bash Reference Manual (gnu.org/software/bash/manual): the shell-and-scripting foundation, control flow and functions, the robustness practices that separate a script that works from one that survives, and the expansion machinery that explains the shell's surprises. Scoped to writing correct, robust scripts — interactive-shell customization, job control, and completion programming are out of scope. 29 nodes across 6 branches, foundations-first with each branch unlocking the next.

---

## Node definitions

29 nodes across 6 branches.

### [ROOT] Bash foundations (always unlocked — 5 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|-----------|-----|
| What Bash is: shell and scripting language | Can explain that bash is both an interactive shell and a script interpreter, and articulate where a shell script is the right tool versus where a general-purpose language fits better | Qualitative | None | https://www.gnu.org/software/bash/manual/html_node/What-is-Bash_003f.html | bash-what-bash-is-shell-and-scripting-language |
| Writing and running a script: shebang, chmod, invocation | Has written a script with a `#!/usr/bin/env bash` shebang, made it executable, and can distinguish `./script`, `bash script`, and `source script` | Exercise / Historical | shell scripts present → `[~\|artifact]` | https://www.gnu.org/software/bash/manual/html_node/Shell-Scripts.html | bash-writing-and-running-a-script-shebang-chmod-invocation |
| Variables and assignment | Assigns with `name=value` (no spaces), reads with `$name`/`${name}`, and can explain the difference between a shell variable and an exported environment variable | Exercise / Qualitative | None | https://www.gnu.org/software/bash/manual/html_node/Shell-Parameters.html | bash-variables-and-assignment |
| Quoting: single, double, and why it matters | Can explain the difference between `'single'`, `"double"`, and unquoted text, and connect quoting to preventing word splitting and globbing | Qualitative | None | https://www.gnu.org/software/bash/manual/html_node/Quoting.html | bash-quoting-single-double-and-why-it-matters |
| Exit status and command success | Can explain that every command returns a status (`0` = success), reads `$?`, uses `exit N`, and knows `true`/`false` | Qualitative / Exercise | None | https://www.gnu.org/software/bash/manual/html_node/Exit-Status.html | bash-exit-status-and-command-success |

### [A] Control flow (5 nodes, unlocks when ROOT ≥ 3 `[✓]`)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|-----------|-----|
| Conditionals: if, test, and [[ ]] | Can write an `if` using `[[ ]]`, explain how it differs from `[ ]`/`test`, and name a reason `[[ ]]` is safer in bash (no word-splitting, pattern/regex matching) | Qualitative / Exercise | None | https://www.gnu.org/software/bash/manual/html_node/Bash-Conditional-Expressions.html | bash-conditionals-if-test-and |
| Case statements | Uses a `case` statement for multi-pattern dispatch and can explain when it reads more cleanly than an `if`/`elif` chain | Exercise / Qualitative | None | https://www.gnu.org/software/bash/manual/html_node/Conditional-Constructs.html | bash-case-statements |
| Loops: for, while, until | Writes `for`, `while`, and `until` loops; iterates a list and reads a stream line by line, and knows the `while read` idiom | Exercise | None | https://www.gnu.org/software/bash/manual/html_node/Looping-Constructs.html | bash-loops-for-while-until |
| Lists and short-circuits: &&, \|\|, ; | Can explain command lists and how `&&`/`\|\|` chain on exit status, and writes a correct `cmd1 && cmd2 \|\| fallback` | Qualitative | None | https://www.gnu.org/software/bash/manual/html_node/Lists.html | bash-lists-and-short-circuits |
| Integer arithmetic: (( )) and $(( )) | Does integer math with `(( ))` and `$(( ))`, uses arithmetic comparisons, and knows bash has no native floats | Exercise | None | https://www.gnu.org/software/bash/manual/html_node/Shell-Arithmetic.html | bash-integer-arithmetic-and |

### [B] Functions and parameters (5 nodes, unlocks when Branch A ≥ 3 `[✓]`)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|-----------|-----|
| Defining and calling functions | Defines a function with `name() { ... }`, calls it, passes arguments, and structures a script around functions | Exercise | shell functions in scripts → `[~\|artifact]` | https://www.gnu.org/software/bash/manual/html_node/Shell-Functions.html | bash-defining-and-calling-functions |
| Positional parameters and "$@" vs "$*" | Accesses `$1`…`$#` and can explain the critical difference between `"$@"` and `"$*"` when forwarding arguments | Qualitative / Exercise | None | https://www.gnu.org/software/bash/manual/html_node/Positional-Parameters.html | bash-positional-parameters-and-vs |
| Special parameters and function exit status | Knows `$?`, `$$`, `$0`, and can explain `return N` (function status) versus `exit N` (whole script) | Qualitative | None | https://www.gnu.org/software/bash/manual/html_node/Special-Parameters.html | bash-special-parameters-and-function-exit-status |
| Local variables and scope | Can explain that bash variables are global by default, uses `local` inside functions, and knows why leaking globals causes bugs | Qualitative / Exercise | None | https://www.gnu.org/software/bash/manual/html_node/Shell-Functions.html | bash-local-variables-and-scope |
| Reading input with read | Reads input with `read` (and knows to use `read -r`), and can write a `while read -r line` loop over stdin | Exercise | None | https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html | bash-reading-input-with-read |

### [C] Robustness and safety (5 nodes, unlocks when Branch B ≥ 2 `[✓]`)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|-----------|-----|
| Strict mode: set -e, -u, -o pipefail | Can explain what each of `set -e`, `set -u`, and `set -o pipefail` does, and name a case where `set -e` does *not* abort as expected | Qualitative | `set -e` in scripts → `[~\|artifact]` | https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html | bash-strict-mode-set-e-u-o-pipefail |
| Quoting pitfalls and word splitting | Can explain word splitting — why an unquoted `$var` can become several arguments — and defaults to quoting expansions to prevent it. The single biggest source of shell bugs | Qualitative | None | https://www.gnu.org/software/bash/manual/html_node/Word-Splitting.html | bash-quoting-pitfalls-and-word-splitting |
| Traps and cleanup: trap ... EXIT | Uses `trap` to run cleanup (e.g. remove a temp file) on `EXIT` or on an error signal, and can explain why that beats cleanup at the end of the script | Exercise / Qualitative | None | https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html | bash-traps-and-cleanup-trap-exit |
| Error handling patterns | Checks exit status explicitly, uses the `cmd \|\| { echo ...; exit 1; }` pattern, and knows where `set -e` silently won't save them | Qualitative | None | https://www.gnu.org/software/bash/manual/html_node/Exit-Status.html | bash-error-handling-patterns |
| Linting with ShellCheck | Knows ShellCheck catches quoting and robustness bugs bash won't warn about, and has run it on a script or wired it into CI | Artifact / Qualitative | `.shellcheckrc` present → `[~\|artifact]` | https://www.shellcheck.net/ | bash-linting-with-shellcheck |

### [D] Expansions and I/O (5 nodes, unlocks when Branch C ≥ 2 `[✓]`)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|-----------|-----|
| Parameter expansion | Uses `${var:-default}`, distinguishes it from `${var:=default}`, and reaches for at least one of length (`${#var}`), trim (`${var#pat}`), or replace (`${var/a/b}`) | Exercise / Qualitative | None | https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html | bash-parameter-expansion |
| Command substitution: $(...) | Captures a command's output into a variable with `$(...)`, and can explain why it is preferred over backticks (nesting, readability) | Exercise | None | https://www.gnu.org/software/bash/manual/html_node/Command-Substitution.html | bash-command-substitution |
| Redirection: stdout, stderr, and /dev/null | Redirects stdout with `>`/`>>`, merges stderr with `2>&1`, and discards output to `/dev/null`; can explain the `2>&1` ordering gotcha | Exercise / Qualitative | None | https://www.gnu.org/software/bash/manual/html_node/Redirections.html | bash-redirection-stdout-stderr-and-dev-null |
| Pipes and pipelines | Composes commands with `\|`, can explain that a pipeline's status is its last command by default, and knows `pipefail` changes that | Exercise | None | https://www.gnu.org/software/bash/manual/html_node/Pipelines.html | bash-pipes-and-pipelines |
| Here-documents and here-strings | Uses a here-document (`<<EOF`) to feed multi-line input, and can distinguish `<<EOF`, `<<-EOF` (tab-stripping), and a here-string `<<<` | Exercise | None | https://www.gnu.org/software/bash/manual/html_node/Redirections.html | bash-here-documents-and-here-strings |

### [E] Advanced (4 nodes, unlocks when Branch D ≥ 2 `[✓]`)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|-----------|-----|
| Arrays: indexed and associative | Declares and iterates an indexed array, knows `"${arr[@]}"` is the correct quoted iteration form, and knows associative arrays (`declare -A`) exist and what they're for | Exercise / Qualitative | None | https://www.gnu.org/software/bash/manual/html_node/Arrays.html | bash-arrays-indexed-and-associative |
| Globbing and brace expansion | Can distinguish filename globbing (`*`, `?`, `[...]`) from brace expansion (`{a,b}`) — one matches existing files, the other generates text — and knows a glob matching nothing stays literal by default | Qualitative | None | https://www.gnu.org/software/bash/manual/html_node/Filename-Expansion.html | bash-globbing-and-brace-expansion |
| Process substitution: <(...) | Uses `<(command)` to feed a command's output where a filename is expected (e.g. `diff <(a) <(b)`) and can explain what bash provides under the hood | Qualitative / Exercise | None | https://www.gnu.org/software/bash/manual/html_node/Process-Substitution.html | bash-process-substitution |
| Expansion order and the expansion pipeline | Can name several of the shell's expansions in order (brace → tilde → parameter → command → arithmetic → word-splitting → filename) and explain how the order accounts for a surprising result | Qualitative | None | https://www.gnu.org/software/bash/manual/html_node/Shell-Expansions.html | bash-expansion-order-and-the-expansion-pipeline |

---

## Probes

| name | primitive | args |
|------|-----------|------|
| shell_scripts    | glob-count  | **/*.sh --exclude **/node_modules/** |
| bash_shebang     | grep-count  | "#!.*bash" scripts bin hooks |
| strict_mode      | grep-count  | "set -e" scripts bin hooks |
| shell_functions  | grep-count  | "\(\) *\{" scripts bin hooks |
| shellcheck_config | file-exists | .shellcheckrc |

Notes: `shell_scripts` counts `.sh` files anywhere in the tree (recursive glob), excluding `node_modules/` trees at any depth — vendored packages ship `.sh` files that would otherwise seed a false `[~]`. The three `grep-count` probes scope their search to conventional script homes (`scripts`, `bin`, `hooks`) rather than the whole repo — a non-existent path safely contributes 0, so this biases toward precision (a miss just means "no seed", the gap question still covers the node) over recall. `bash_shebang` matches a bash shebang line; `strict_mode` matches `set -e` (which also occurs inside `set -euo pipefail`); `shell_functions` matches a `() {` function-body opener. All are best-effort seeds that raise `[~]`, never a false `[✓]`.

---

## Detection signals

| Collected evidence | Node → status |
|--------------------|---------------|
| shell_scripts > 0 | ROOT: "Writing and running a script: shebang, chmod, invocation" → `[~\|artifact]` |
| bash_shebang > 0 | ROOT: "Writing and running a script: shebang, chmod, invocation" → `[~\|artifact]` |
| shell_functions > 0 | B: "Defining and calling functions" → `[~\|artifact]` |
| strict_mode > 0 | C: "Strict mode: set -e, -u, -o pipefail" → `[~\|artifact]` |
| shellcheck_config exists | C: "Linting with ShellCheck" → `[~\|artifact]` |

---

## Gap questions

| Branch | Gap | Ask this |
|--------|-----|----------|
| [ROOT] | What bash is | "When would you reach for a bash script versus a language like Python? What is bash genuinely good at, and where does it start to hurt?" |
| [ROOT] | Running a script | "You've written a script file. Walk me through everything needed to run it as `./myscript` — the first line, the permission — and how that differs from `bash myscript` or `source myscript`." |
| [ROOT] | Variables | "How do you assign a variable in bash, and what's the one spacing mistake everyone makes at first? How does a shell variable differ from an exported environment variable?" |
| [ROOT] | Quoting | "You have `name='a b c'`. Explain what happens with `rm $name` versus `rm \"$name\"`, and the general rule you follow for when to quote." |
| [ROOT] | Exit status | "How does bash know whether a command succeeded? What is `$?`, and how would you make your own script exit with a failure code?" |
| [A] | Conditionals | "Explain the difference between `[ ]`, `test`, and `[[ ]]`. Why is `[[ ]]` preferred in bash, and name one thing it handles more safely." |
| [A] | Case | "You need to branch on a variable across several patterns. Why might `case` read more cleanly than a chain of `if`/`elif`? Sketch one." |
| [A] | Loops | "Show me how you'd loop over a list of arguments versus over the lines of a file. Which loop each time, and what's the gotcha when reading lines?" |
| [A] | Lists / short-circuits | "Explain what `cmd1 && cmd2 \|\| cmd3` does step by step. Give a real one-liner you'd actually write with `&&` and `\|\|`." |
| [A] | Arithmetic | "How do you do integer math in bash? What's the difference between `(( ))` and `$(( ))`, and what happens if you try to divide to get a fraction?" |
| [B] | Functions | "How do you define a function in bash and call it? How do arguments get in, and how does a function hand back a value or a success/failure status?" |
| [B] | Positional / "$@" | "Inside a script, how do you get at its arguments? Explain the difference between `\"$@\"` and `\"$*\"` — why does the quoting matter when you forward args to another command?" |
| [B] | Special params | "What do `$?`, `$$`, and `$0` give you? Inside a function, what's the difference between `return 1` and `exit 1`?" |
| [B] | Scope | "By default, is a variable set inside a function global or local to that function? What does `local` change, and why does it matter in a bigger script?" |
| [B] | Reading input | "How do you read a line of input into a variable? Why do you almost always want `read -r`, and how would you loop over stdin line by line?" |
| [C] | Strict mode | "Walk me through `set -euo pipefail` — what does each of the three do? And name one situation where `set -e` does *not* abort like you'd expect." |
| [C] | Word splitting | "Explain word splitting. Why does an unquoted `$var` sometimes turn one value into several arguments, and how does quoting prevent it?" |
| [C] | Traps | "How do you make sure a temp file gets cleaned up even if your script exits early or errors out? Explain `trap` and which signal or pseudo-signal you'd trap." |
| [C] | Error handling | "Besides `set -e`, how do you handle a command that might fail? Show the `cmd \|\| { …; exit 1; }` pattern and when you'd reach for it." |
| [C] | ShellCheck | "What is ShellCheck, and what class of bugs does it catch that bash itself won't warn you about? Have you run it on a script or wired it into CI?" |
| [D] | Parameter expansion | "Explain `${VAR:-default}` and how it differs from `${VAR:=default}`. Give one other parameter expansion you use — a length, a trim, or a replace." |
| [D] | Command substitution | "How do you capture a command's output into a variable? Why is `$(...)` preferred over backticks, especially when you nest them?" |
| [D] | Redirection | "How do you send stdout to a file, send stderr to the same place, and throw output away entirely? Explain `2>&1` and its ordering gotcha." |
| [D] | Pipelines | "What does a pipe actually connect? In `a \| b \| c`, if `a` fails, does the whole pipeline fail? How does `pipefail` change the answer?" |
| [D] | Here-docs | "When would you use a here-document (`<<EOF`)? What's the difference between `<<EOF`, `<<-EOF`, and a here-string `<<<`?" |
| [E] | Arrays | "How do you declare and iterate an indexed array in bash? Why is `\"${arr[@]}\"` the correct way to loop over it, and what's an associative array for?" |
| [E] | Globbing / brace | "Explain the difference between a glob like `*.txt` and brace expansion like `{a,b}.txt` — which one matches existing files and which just generates text? What happens when a glob matches nothing?" |
| [E] | Process substitution | "What does `<(command)` give you? Show a case where you'd use `diff <(cmd1) <(cmd2)`, and explain what bash is doing under the hood." |
| [E] | Expansion order | "Bash runs several expansions in a fixed order before executing a command. Name a few in order, and explain how that order accounts for a surprising result you've hit." |

### Qualitative rubric

- **`[✓]` Demonstrated**: Contains at least one specific, verifiable detail — the actual flag or syntax, an observed behavior, a bug navigated, or a causal explanation of *why*, not just *what*.
- **`[~]` Self-reported**: Affirmative but vague. "Yeah, I write loops and functions" with no mechanism or scenario.
- **`[ ]` Not yet**: Negative, "not sure," or "heard of it but haven't done it."

### Answer → node mapping

| Answer contains | Node → status |
|-----------------|---------------|
| Bash's niche (glue/automation) vs. a real language, with a tradeoff | ROOT: "What Bash is: shell and scripting language" → `[✓\|reported]` |
| Shebang + `chmod +x` + `./` vs `bash` vs `source` distinguished | ROOT: "Writing and running a script: shebang, chmod, invocation" → `[✓\|reported]` |
| `name=value` no-spaces rule + shell vs. exported env var | ROOT: "Variables and assignment" → `[✓\|reported]` |
| Single vs. double vs. unquoted, tied to word splitting/globbing | ROOT: "Quoting: single, double, and why it matters" → `[✓\|reported]` |
| `$?` / `0`-is-success / `exit N` explained | ROOT: "Exit status and command success" → `[✓\|reported]` |
| `[[ ]]` vs `[ ]` distinction + a concrete safety/feature reason | A: "Conditionals: if, test, and [[ ]]" → `[✓\|reported]` |
| A real `case` used for multi-pattern dispatch | A: "Case statements" → `[✓\|reported]` |
| `for`/`while`/`until` used correctly + the `while read` line gotcha | A: "Loops: for, while, until" → `[✓\|reported]` |
| `&&`/`\|\|` short-circuit semantics + a real one-liner | A: "Lists and short-circuits: &&, \|\|, ;" → `[✓\|reported]` |
| `(( ))` vs `$(( ))` + the no-floats point | A: "Integer arithmetic: (( )) and $(( ))" → `[✓\|reported]` |
| Function defined/called + args in + return/status out | B: "Defining and calling functions" → `[✓\|reported]` |
| `"$@"` vs `"$*"` difference explained with the quoting reason | B: "Positional parameters" → `[✓\|reported]` |
| `$?`/`$$`/`$0` + `return` vs `exit` distinction | B: "Special parameters and function exit status" → `[✓\|reported]` |
| Global-by-default + `local` fixes it, with why | B: "Local variables and scope" → `[✓\|reported]` |
| `read -r` (and why) + a `while read` stdin loop | B: "Reading input with read" → `[✓\|reported]` |
| Each of `-e`/`-u`/`-o pipefail` explained + a `set -e` blind spot | C: "Strict mode: set -e, -u, -o pipefail" → `[✓\|reported]` |
| Word splitting mechanism + quoting as the fix | C: "Quoting pitfalls and word splitting" → `[✓\|reported]` |
| `trap ... EXIT` for cleanup + why it beats end-of-script cleanup | C: "Traps and cleanup: trap ... EXIT" → `[✓\|reported]` |
| Explicit status checks / `\|\| { …; exit 1; }` + a `set -e` gap | C: "Error handling patterns" → `[✓\|reported]` |
| ShellCheck's purpose + a bug class it catches (or CI wiring) | C: "Linting with ShellCheck" → `[✓\|reported]` |
| `${var:-}` vs `${var:=}` + one more expansion (length/trim/replace) | D: "Parameter expansion" → `[✓\|reported]` |
| `$(...)` capture + why over backticks (nesting) | D: "Command substitution: $(...)" → `[✓\|reported]` |
| `>`/`>>`/`2>&1`/`/dev/null` + the `2>&1` ordering gotcha | D: "Redirection: stdout, stderr, and /dev/null" → `[✓\|reported]` |
| Pipe semantics + last-command status + `pipefail` effect | D: "Pipes and pipelines" → `[✓\|reported]` |
| Here-doc usage + `<<EOF` vs `<<-EOF` vs `<<<` distinguished | D: "Here-documents and here-strings" → `[✓\|reported]` |
| Indexed array iteration + `"${arr[@]}"` + associative purpose | E: "Arrays: indexed and associative" → `[✓\|reported]` |
| Glob (matches files) vs. brace (generates text) + empty-glob behavior | E: "Globbing and brace expansion" → `[✓\|reported]` |
| `<(...)` for a file-expecting command + a real `diff` use | E: "Process substitution: <(...)" → `[✓\|reported]` |
| Several expansions named in order + why the order explains a result | E: "Expansion order and the expansion pipeline" → `[✓\|reported]` |

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
Bash Foundations
    [?] What Bash is: shell and scripting language
    [?] Writing and running a script: shebang, chmod, invocation
    [?] Variables and assignment
    [?] Quoting: single, double, and why it matters
    [?] Exit status and command success

Control Flow   [if locked: "(unlock: complete 3 Bash Foundations)"]
    [?] Conditionals: if, test, and [[ ]]
    [?] Case statements
    [?] Loops: for, while, until
    [?] Lists and short-circuits: &&, ||, ;
    [?] Integer arithmetic: (( )) and $(( ))

Functions and Parameters   [if locked: "(unlock: complete 3 Control Flow skills)"]
    [?] Defining and calling functions
    [?] Positional parameters and "$@" vs "$*"
    [?] Special parameters and function exit status
    [?] Local variables and scope
    [?] Reading input with read

Robustness and Safety   [if locked: "(unlock: complete 2 Functions and Parameters skills)"]
    [?] Strict mode: set -e, -u, -o pipefail
    [?] Quoting pitfalls and word splitting
    [?] Traps and cleanup: trap ... EXIT
    [?] Error handling patterns
    [?] Linting with ShellCheck

Expansions and I/O   [if locked: "(unlock: complete 2 Robustness and Safety skills)"]
    [?] Parameter expansion
    [?] Command substitution: $(...)
    [?] Redirection: stdout, stderr, and /dev/null
    [?] Pipes and pipelines
    [?] Here-documents and here-strings

Advanced   [if locked: "(unlock: complete 2 Expansions and I/O skills)"]
    [?] Arrays: indexed and associative
    [?] Globbing and brace expansion
    [?] Process substitution: <(...)
    [?] Expansion order and the expansion pipeline
```

---

## Saved tree file template

```markdown
---
version: 3
topic: bash
user: [git config user.name or "unknown"]
email: [git config user.email or "unknown"]
updated: [today's date YYYY-MM-DD]
level: [Explorer / Builder / Practitioner / Expert]
xp: [CURRENT_XP]
---

# Bash Knowledge Graph

*[✓] Demonstrated · [~] Self-reported · [ ] Not yet · [★] Mastery target · [·] Locked*

## [ROOT] Bash Foundations
- [STATUS|TYPE] What Bash is: shell and scripting language
- [STATUS|TYPE] Writing and running a script: shebang, chmod, invocation
- [STATUS|TYPE] Variables and assignment
- [STATUS|TYPE] Quoting: single, double, and why it matters
- [STATUS|TYPE] Exit status and command success

## [A] Control Flow
- [STATUS|TYPE] Conditionals: if, test, and [[ ]]
- [STATUS|TYPE] Case statements
- [STATUS|TYPE] Loops: for, while, until
- [STATUS|TYPE] Lists and short-circuits: &&, ||, ;
- [STATUS|TYPE] Integer arithmetic: (( )) and $(( ))

## [B] Functions and Parameters
- [STATUS|TYPE] Defining and calling functions
- [STATUS|TYPE] Positional parameters and "$@" vs "$*"
- [STATUS|TYPE] Special parameters and function exit status
- [STATUS|TYPE] Local variables and scope
- [STATUS|TYPE] Reading input with read

## [C] Robustness and Safety
- [STATUS|TYPE] Strict mode: set -e, -u, -o pipefail
- [STATUS|TYPE] Quoting pitfalls and word splitting
- [STATUS|TYPE] Traps and cleanup: trap ... EXIT
- [STATUS|TYPE] Error handling patterns
- [STATUS|TYPE] Linting with ShellCheck

## [D] Expansions and I/O
- [STATUS|TYPE] Parameter expansion
- [STATUS|TYPE] Command substitution: $(...)
- [STATUS|TYPE] Redirection: stdout, stderr, and /dev/null
- [STATUS|TYPE] Pipes and pipelines
- [STATUS|TYPE] Here-documents and here-strings

## [E] Advanced
- [STATUS|TYPE] Arrays: indexed and associative
- [STATUS|TYPE] Globbing and brace expansion
- [STATUS|TYPE] Process substitution: <(...)
- [STATUS|TYPE] Expansion order and the expansion pipeline

## Frontier
- [frontier node name] — [criterion one-liner]

## Notes
<!-- Add personal notes here -->
```
