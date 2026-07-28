---
topic: python
node_count: 31
version: 1
source_url: https://docs.python.org/3/tutorial/index.html
goal: ramp them up on Python as a working language — reading and writing idiomatic code with a firm grip on the object model, functions and scope, the workhorse containers, classes, and the robustness constructs (exceptions, context managers, generators, decorators) that production code relies on
description: Python language fundamentals — the object model, control flow, functions and scope, core containers, classes and the object protocol, and robustness constructs. Grounded in the official Python Tutorial and Language Reference.
---

# Python Knowledge Graph Schema

This file defines the curriculum for the `python` topic. It follows the official Python Tutorial (docs.python.org/3/tutorial/) with the Language Reference and `library/stdtypes` behind it: the object model and core types first, then control flow and iteration, functions and scope, the workhorse containers, classes and the object protocol, and the robustness constructs production code leans on. 31 nodes across 6 branches, foundations-first with each branch unlocking the next.

**Deliberately out of scope** (each would be a later additive branch or its own sibling topic, not a missing node here): `async`/`await` and concurrency (threads, multiprocessing, the GIL); descriptors, metaclasses, and `__slots__`; standard-library module fluency (`pathlib`, `collections`, `itertools`, `dataclasses`, …); typing beyond built-in annotations (generics, protocols, checker practice); packaging, virtual environments, and dependency management.

---

## Node definitions

31 nodes across 6 branches.

### [ROOT] Objects and names (always unlocked — 5 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|-----------|-----|
| Objects, types, and names as bindings | Can explain that every value is an object with a type (`type()`), that assignment binds a name to an object rather than filling a "box" — and can predict aliasing: after `b = a`, a mutation through `b` is visible through `a` | Qualitative | Python files present → `[~\|artifact]` | https://docs.python.org/3/reference/datamodel.html#objects-values-and-types | python-objects-types-and-names-as-bindings |
| Mutability and copying | Can classify the core built-ins as mutable (list, dict, set) vs. immutable (int, str, tuple), state one consequence of each (aliasing bugs; dict-key eligibility), and choose shallow vs. deep copy knowing a shallow copy shares nested objects | Qualitative | None | https://docs.python.org/3/library/copy.html | python-mutability-and-copying |
| Numbers and arithmetic | Uses int and float with the right operators — `/` always yields a float, `//` floors, `%` for modulo, `**` for powers — and can explain why `0.1 + 0.2 == 0.3` is False (binary float representation) and what to do when it matters | Qualitative / Exercise | None | https://docs.python.org/3/tutorial/introduction.html#numbers | python-numbers-and-arithmetic |
| Strings and f-strings | Slices and manipulates strings knowing they are immutable sequences (methods return new strings), and formats with f-strings including format specs (`f"{price:.2f}"`) | Exercise / Qualitative | None | https://docs.python.org/3/tutorial/introduction.html#text | python-strings-and-f-strings |
| Truthiness, None, and identity vs. equality | Can enumerate the falsy built-ins (`None`, `False`, zeros, empty strings and containers), explain `is` (identity) vs. `==` (equality), and why `x is None` is the idiom while `is` between numbers or strings is a trap | Qualitative | None | https://docs.python.org/3/library/stdtypes.html#truth-value-testing | python-truthiness-none-and-identity-vs-equality |

### [A] Control flow and iteration (5 nodes, unlocks when ROOT ≥ 3 `[✓]`)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|-----------|-----|
| Conditionals and guard clauses | Writes `if`/`elif`/`else` and the conditional expression (`x if cond else y`); flattens nested conditionals into early-return guard clauses and can say why that reads better | Exercise / Qualitative | None | https://docs.python.org/3/tutorial/controlflow.html#if-statements | python-conditionals-and-guard-clauses |
| for loops and the iteration protocol | Can explain that `for` iterates any iterable directly (no index bookkeeping), reaches for `enumerate` and `zip` instead of `range(len(...))`, and knows why mutating a collection while iterating it misbehaves | Exercise / Qualitative | None | https://docs.python.org/3/tutorial/controlflow.html#for-statements | python-for-loops-and-the-iteration-protocol |
| while, break, continue, and loop else | Uses `while` with `break`/`continue` deliberately, and can state the loop-`else` rule — the `else` suite runs only when the loop ends without `break` — with a search-loop use case | Qualitative / Exercise | None | https://docs.python.org/3/tutorial/controlflow.html#else-clauses-on-loops | python-while-break-continue-and-loop-else |
| Comprehensions | Converts filter-and-transform loops into list/dict/set comprehensions (with conditions), and can judge when a comprehension hurts — side effects, or nesting deep enough that the loop reads better | Exercise / Qualitative | None | https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions | python-comprehensions |
| Structural pattern matching with match | Uses `match`/`case` with literal, sequence, and class patterns — and can explain the capture trap: a bare name in a pattern binds, it does not compare against an existing constant | Qualitative / Exercise | None | https://docs.python.org/3/tutorial/controlflow.html#match-statements | python-structural-pattern-matching-with-match |

### [B] Functions and scope (6 nodes, unlocks when Branch A ≥ 3 `[✓]`)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|-----------|-----|
| Defining functions; functions as objects | Defines functions with `def`, knows a function without `return` yields `None`, and treats functions as first-class objects — passing them as arguments or storing them in a dict as a dispatch table | Exercise / Qualitative | function definitions in repo → `[~\|artifact]` | https://docs.python.org/3/tutorial/controlflow.html#defining-functions | python-defining-functions-functions-as-objects |
| Parameters and default values | Uses positional and keyword arguments fluently — and can explain the mutable-default trap: defaults are evaluated once at `def` time, so `def f(acc=[])` shares one list across calls; states the `None`-sentinel fix | Qualitative | None | https://docs.python.org/3/tutorial/controlflow.html#default-argument-values | python-parameters-and-default-values |
| *args, **kwargs, and unpacking calls | Can explain what `*args` and `**kwargs` collect in a signature, unpacks sequences and dicts into calls with `*`/`**`, and forces keyword-only parameters with a bare `*` | Exercise / Qualitative | None | https://docs.python.org/3/tutorial/controlflow.html#arbitrary-argument-lists | python-args-kwargs-and-unpacking-calls |
| Scopes: LEGB, closures, and nonlocal | Can walk the local → enclosing → global → builtins resolution order, explain that closures capture variables not values (the late-binding loop gotcha) and a fix for it, and say what `nonlocal`/`global` change | Qualitative | None | https://docs.python.org/3/tutorial/classes.html#python-scopes-and-namespaces | python-scopes-legb-closures-and-nonlocal |
| lambda and higher-order functions | Uses `lambda` as a `key=` for `sorted`/`min`/`max`, knows a lambda is limited to a single expression, and can say where a named `def` becomes the better choice | Exercise / Qualitative | None | https://docs.python.org/3/tutorial/controlflow.html#lambda-expressions | python-lambda-and-higher-order-functions |
| Docstrings and annotations | Writes docstrings (summary first line) where tooling finds them (`help()`, `__doc__`), and can explain that annotations (`def f(x: int) -> str:`) are metadata — not enforced at runtime, consumed by type checkers and readers | Artifact / Qualitative | return annotations in repo → `[~\|artifact]` | https://docs.python.org/3/tutorial/controlflow.html#documentation-strings | python-docstrings-and-annotations |

### [C] Workhorse containers (4 nodes, unlocks when Branch B ≥ 4 `[✓]`)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|-----------|-----|
| Lists in practice | Uses append/extend/insert/pop and slice assignment; can explain `xs.sort()` (in-place, returns `None`) vs. `sorted(xs)` (new list) — and why `x = xs.sort()` is a classic bug | Exercise / Qualitative | None | https://docs.python.org/3/tutorial/datastructures.html#more-on-lists | python-lists-in-practice |
| Tuples and unpacking | Uses tuples as immutable records; unpacks in assignments and loops including starred targets (`first, *rest = xs`) — and knows the comma makes the tuple: `(1)` is an int, `1,` is a tuple | Exercise / Qualitative | None | https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences | python-tuples-and-unpacking |
| Dictionaries in practice | Chooses between `d[k]` (raises `KeyError`), `d.get(k, default)`, and `d.setdefault` deliberately; iterates with `.items()`; knows keys must be hashable and that insertion order is preserved | Exercise / Qualitative | None | https://docs.python.org/3/tutorial/datastructures.html#dictionaries | python-dictionaries-in-practice |
| Sets and set operations | Reaches for a set for dedup and fast membership; uses union/intersection/difference; knows `{}` is an empty dict — `set()` makes the empty set — and when `frozenset` is required | Exercise / Qualitative | None | https://docs.python.org/3/tutorial/datastructures.html#sets | python-sets-and-set-operations |

### [D] Classes and the object protocol (5 nodes, unlocks when Branch C ≥ 2 `[✓]`)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|-----------|-----|
| Classes, instances, and __init__ | Has defined a class with `__init__` setting instance attributes via `self` — and can explain the class-attribute trap: a mutable class attribute (`items = []` at class level) is shared across all instances | Artifact / Qualitative | class definitions in repo → `[~\|artifact]` | https://docs.python.org/3/tutorial/classes.html#a-first-look-at-classes | python-classes-instances-and-init |
| Methods and properties | Can explain how `obj.method()` binds `self`, and uses `@property` to expose a computed value as attribute access — stating when a property beats a getter method and when it shouldn't hide heavy work | Qualitative / Artifact | None | https://docs.python.org/3/tutorial/classes.html#method-objects | python-methods-and-properties |
| Inheritance and super() | Subclasses and overrides methods, calling `super().__init__()` in the override and can say why `super()` beats naming the parent class; can articulate when composition is the better design | Qualitative / Artifact | None | https://docs.python.org/3/tutorial/classes.html#inheritance | python-inheritance-and-super |
| Dunder methods and the object protocol | Can explain that operators and built-ins dispatch to special methods (`len()` → `__len__`, `==` → `__eq__`, printing → `__repr__`/`__str__`), and implements `__repr__` on their own classes for debuggability | Qualitative / Artifact | None | https://docs.python.org/3/reference/datamodel.html#special-method-names | python-dunder-methods-and-the-object-protocol |
| Iterators from the object side | Can explain the protocol a `for` loop drives — `iter()` → `__iter__`, `next()` → `__next__`, `StopIteration` ends it — and the iterable/iterator distinction: a list can be looped twice, an iterator exhausts | Qualitative | None | https://docs.python.org/3/tutorial/classes.html#iterators | python-iterators-from-the-object-side |

### [E] Robustness and structure (6 nodes, unlocks when Branch D ≥ 3 `[✓]`)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|-----------|-----|
| Handling exceptions | Catches specific exceptions with `try`/`except` and can explain why a bare `except:` is harmful, what `else` adds over widening the `try` body, and what `finally` guarantees | Exercise / Qualitative | None | https://docs.python.org/3/tutorial/errors.html#handling-exceptions | python-handling-exceptions |
| Raising and designing exceptions | Raises with `raise`, defines custom exceptions subclassing `Exception`, and chains with `raise NewError(...) from err`; can say when raising beats returning a sentinel value | Qualitative / Artifact | None | https://docs.python.org/3/tutorial/errors.html#raising-exceptions | python-raising-and-designing-exceptions |
| Context managers and with | Uses `with` for resource cleanup and can explain the guarantee — `__exit__` runs even when the body raises; has written a context manager via `__enter__`/`__exit__` or `contextlib.contextmanager` | Exercise / Qualitative | None | https://docs.python.org/3/reference/compound_stmts.html#the-with-statement | python-context-managers-and-with |
| Generators and yield | Writes generator functions and can explain the model: calling one executes no body code — it returns a lazy, single-pass iterator that resumes at each `yield`; names the memory win and the exhaustion catch | Exercise / Qualitative | `yield` in repo code → `[~\|artifact]` | https://docs.python.org/3/tutorial/classes.html#generators | python-generators-and-yield |
| Decorators | Can explain what `@decorator` above a `def` literally does (rebinds the name to the wrapper's return), writes a wrapper decorator, and knows why `functools.wraps` matters (preserving name and docstring) | Exercise / Qualitative | decorator lines in repo → `[~\|artifact]` | https://docs.python.org/3/glossary.html#term-decorator | python-decorators |
| Modules, imports, and the __main__ guard | Structures code as importable modules; can explain what `if __name__ == "__main__":` distinguishes (script run vs. import) and why import-time side effects are a smell | Artifact / Qualitative | `__main__` guard in repo → `[~\|artifact]` | https://docs.python.org/3/tutorial/modules.html | python-modules-imports-and-the-main-guard |

---

## Probes

| name | primitive | args |
|------|-----------|------|
| python_files        | glob-count | **/*.py --exclude venv/** |
| class_defs          | grep-count | "^class " src lib app tests scripts |
| func_defs           | grep-count | "^def " src lib app tests scripts |
| decorator_lines     | grep-count | "^ *@" src lib app tests scripts |
| return_annotations  | grep-count | "-> " src lib app tests scripts |
| yield_lines         | grep-count | "yield" src lib app tests scripts |
| main_guards         | grep-count | "__main__" src lib app tests scripts |

Notes: `python_files` uses a recursive glob, which does not descend into dot-directories — a `.venv/` is invisible to it — and the explicit `--exclude venv/**` removes unhidden virtual environments, so the signal means *project* Python, not vendored interpreters. The grep probes scan the conventional source roots (`src lib app tests scripts`) precisely so vendored and virtual-environment code never counts; a missing path yields 0 (precision bias — a signal that under-fires beats one that false-positives). `decorator_lines` matches any line whose first non-blank character is `@`, which in Python source is a decorator application. `main_guards` matches any `__main__` occurrence, which slightly over-counts (e.g. `python -m` mentions in docstrings) — acceptable because it seeds only `[~]`.

---

## Detection signals

| Collected evidence | Node → status |
|--------------------|---------------|
| python_files > 0 | ROOT: "Objects, types, and names as bindings" → `[~\|artifact]` |
| func_defs > 0 | B: "Defining functions; functions as objects" → `[~\|artifact]` |
| return_annotations > 0 | B: "Docstrings and annotations" → `[~\|artifact]` |
| class_defs > 0 | D: "Classes, instances, and __init__" → `[~\|artifact]` |
| yield_lines > 0 | E: "Generators and yield" → `[~\|artifact]` |
| decorator_lines > 0 | E: "Decorators" → `[~\|artifact]` |
| main_guards > 0 | E: "Modules, imports, and the __main__ guard" → `[~\|artifact]` |

All signals seed `[~|artifact]`, never `[✓]`: code present in a repository is consistent with the user holding these skills but does not directly witness *their* act of writing it (the direct-witness rule) — teach-back verification upgrades from there.

---

## Gap questions

| Branch | Gap | Ask this |
|--------|-----|----------|
| [ROOT] | Names and binding | "After `a = [1, 2]`, then `b = a`, then `b.append(3)` — what does `a` hold, and why? Walk me through what assignment actually does in Python." |
| [ROOT] | Mutability and copying | "You 'copied' a list of lists, edited one inner list, and the copy changed too. What happened, and how do you copy so it doesn't?" |
| [ROOT] | Numbers | "What's the difference between `/` and `//`? And why does `0.1 + 0.2 == 0.3` come out False — what do you do when that matters?" |
| [ROOT] | Strings | "Why doesn't `s.upper()` change `s`? And in an f-string, how do you render a float to two decimal places?" |
| [ROOT] | Truthiness and identity | "When do you write `is` instead of `==`, and why is `x is None` the idiom? Which built-in values count as falsy?" |
| [A] | Conditionals | "You've got an `if` nested three levels deep. How do guard clauses flatten it, and what's Python's one-line conditional expression?" |
| [A] | Iteration | "You need both the index and the value while looping — what do you reach for, and why is `for i in range(len(xs))` considered un-Pythonic?" |
| [A] | Loop else | "A `for` loop can carry an `else` clause — when does it run, when doesn't it, and what's it actually useful for?" |
| [A] | Comprehensions | "Turn 'keep the even numbers, squared' into a comprehension. When do you deliberately write the loop instead?" |
| [A] | match capture | "In a `match` statement, what does a bare name in a pattern like `case found:` do — compare or capture? Why does that make matching against a constant tricky?" |
| [B] | Functions as objects | "What does a function return when there's no `return` statement? And give one practical use of passing a function around as a value." |
| [B] | Default values | "What's wrong with `def f(x, acc=[])`? When exactly is that default evaluated, and what's the standard fix?" |
| [B] | args and kwargs | "In a signature, what do `*args` and `**kwargs` collect? And what does `*` do at the call site — or standing alone in the parameter list?" |
| [B] | Scope and closures | "You build `[lambda: i for i in range(3)]` and every lambda returns 2. Why, and what's the fix? What do `nonlocal` and `global` change?" |
| [B] | lambda | "How do you sort a list of dicts by one field? What is a lambda allowed to contain, and where do you switch to a named `def`?" |
| [B] | Docstrings and annotations | "What does `def f(x: int) -> str:` enforce when the code runs? Who actually consumes annotations — and where does a docstring live so `help()` finds it?" |
| [C] | Lists | "`xs.sort()` versus `sorted(xs)` — what does each return, what does each mutate, and which bug does mixing them up cause?" |
| [C] | Tuples | "How does the one-line swap `a, b = b, a` work? What does `first, *rest = xs` leave in `rest` — and why isn't `(1)` a tuple?" |
| [C] | Dicts | "A key might be missing: when do you use `d[k]`, `d.get(k)`, or `d.setdefault(k, ...)`? And what disqualifies a value from being a dict key?" |
| [C] | Sets | "You need fast membership tests over a big collection with duplicates gone — what do you use and why? And why doesn't `{}` give you an empty set?" |
| [D] | Classes | "What is `self`, mechanically? And what goes wrong when `items = []` sits at class level instead of inside `__init__`?" |
| [D] | Properties | "When do you turn a method into a `@property`? What stays the same for callers, and why shouldn't a property do heavy work?" |
| [D] | Inheritance | "In an overriding `__init__`, why call `super().__init__()` instead of `Parent.__init__(self)`? And when do you skip inheritance for composition?" |
| [D] | Dunders | "How does `len(x)` get its answer? Why implement `__repr__` on your classes, and how does it differ from `__str__`?" |
| [D] | Iterator protocol | "Which two methods make an object an iterator, and how does a `for` loop drive them? Why can a list be looped twice but a generator only once?" |
| [E] | Handling exceptions | "Why is a bare `except:` harmful? In a full `try` statement, what belongs in `else` versus `finally`?" |
| [E] | Raising | "When do you define your own exception class, and what do you inherit from? What does `raise X from err` add over a plain `raise X`?" |
| [E] | Context managers | "What does `with open(...) as f:` guarantee that manual cleanup gets wrong? Which two methods make any object usable in a `with`?" |
| [E] | Generators | "The moment you call a generator function, what has executed? Where does the memory win come from — and what's the one-pass catch?" |
| [E] | Decorators | "What does `@log` above a `def` literally rewrite? Why does a naive wrapper lose the function's name, and what fixes it?" |
| [E] | Modules | "What is `if __name__ == '__main__'` actually testing? What differs between running a file as a script and importing it?" |

### Qualitative rubric

- **`[✓]` Demonstrated**: Contains at least one specific, verifiable detail — the actual syntax/behavior, an observed gotcha, a tradeoff navigated, or a causal explanation of *why*, not just *what*.
- **`[~]` Self-reported**: Affirmative but vague. "Yeah, I use classes" with no mechanism or scenario.
- **`[ ]` Not yet**: Negative, "not sure," or "heard of it but haven't used it."

### Answer → node mapping

| Answer contains | Node → status |
|-----------------|---------------|
| Assignment as name-binding + aliasing predicted (mutation via `b` visible via `a`) | ROOT: "Objects, types, and names as bindings" → `[✓\|reported]` |
| Mutable/immutable classified + shallow-copy sharing of nested objects with the deep-copy fix | ROOT: "Mutability and copying" → `[✓\|reported]` |
| `/` vs. `//` distinguished + binary-float explanation for the 0.1 + 0.2 surprise | ROOT: "Numbers and arithmetic" → `[✓\|reported]` |
| String immutability (methods return new strings) + a working f-string format spec | ROOT: "Strings and f-strings" → `[✓\|reported]` |
| `is` vs. `==` with the `is None` idiom + falsy values enumerated | ROOT: "Truthiness, None, and identity vs. equality" → `[✓\|reported]` |
| Guard-clause flattening shown + the conditional expression | A: "Conditionals and guard clauses" → `[✓\|reported]` |
| `enumerate`/`zip` over `range(len(...))` with the why | A: "for loops and the iteration protocol" → `[✓\|reported]` |
| Loop-`else` runs-only-without-`break` rule + a concrete use | A: "while, break, continue, and loop else" → `[✓\|reported]` |
| A correct comprehension + a case where the loop reads better | A: "Comprehensions" → `[✓\|reported]` |
| Bare-name-binds capture trap explained (dotted/literal patterns compare) | A: "Structural pattern matching with match" → `[✓\|reported]` |
| Implicit `None` return + a first-class-function use (callback or dispatch table) | B: "Defining functions; functions as objects" → `[✓\|reported]` |
| Defaults-evaluated-once at `def` time + the `None`-sentinel fix | B: "Parameters and default values" → `[✓\|reported]` |
| `*args`/`**kwargs` collection + call-site unpacking or keyword-only `*` | B: "*args, **kwargs, and unpacking calls" → `[✓\|reported]` |
| Resolution order walked + late-binding closure gotcha with a fix | B: "Scopes: LEGB, closures, and nonlocal" → `[✓\|reported]` |
| `key=` lambda for sorting + the single-expression limit | B: "lambda and higher-order functions" → `[✓\|reported]` |
| Annotations-not-enforced + who consumes them, docstring placement | B: "Docstrings and annotations" → `[✓\|reported]` |
| `sort()` in-place-returns-`None` vs. `sorted()` new list, with the assignment bug | C: "Lists in practice" → `[✓\|reported]` |
| Tuple unpacking / starred target + comma-makes-the-tuple | C: "Tuples and unpacking" → `[✓\|reported]` |
| `[]` vs. `.get` vs. `setdefault` chosen with reasons + hashable-key rule | C: "Dictionaries in practice" → `[✓\|reported]` |
| Set for dedup/membership with the why + `set()` not `{}` for empty | C: "Sets and set operations" → `[✓\|reported]` |
| `self` explained + shared mutable class-attribute trap | D: "Classes, instances, and __init__" → `[✓\|reported]` |
| `@property` computed-attribute case + unchanged caller syntax | D: "Methods and properties" → `[✓\|reported]` |
| `super().__init__()` cooperation + a composition-over-inheritance judgment | D: "Inheritance and super()" → `[✓\|reported]` |
| Built-in-to-dunder dispatch (`len` → `__len__`) + `__repr__` purpose | D: "Dunder methods and the object protocol" → `[✓\|reported]` |
| `__iter__`/`__next__`/`StopIteration` + iterable-vs-iterator exhaustion | D: "Iterators from the object side" → `[✓\|reported]` |
| Specific-except over bare + `else`/`finally` roles distinguished | E: "Handling exceptions" → `[✓\|reported]` |
| Custom exception subclassing + `raise ... from` chaining | E: "Raising and designing exceptions" → `[✓\|reported]` |
| `__exit__`-even-on-exception guarantee + a written context manager | E: "Context managers and with" → `[✓\|reported]` |
| No-code-runs-at-call + laziness and single-pass exhaustion named | E: "Generators and yield" → `[✓\|reported]` |
| `@` as name rebinding + the `functools.wraps` reason | E: "Decorators" → `[✓\|reported]` |
| Script-vs-import distinction of the `__main__` guard | E: "Modules, imports, and the __main__ guard" → `[✓\|reported]` |

---

## Unlock thresholds

- Branch A unlocks when ROOT ≥ 3 `[✓]`
- Branch B unlocks when Branch A ≥ 3 `[✓]`
- Branch C unlocks when Branch B ≥ 4 `[✓]`
- Branch D unlocks when Branch C ≥ 2 `[✓]`
- Branch E unlocks when Branch D ≥ 3 `[✓]`

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
Objects and Names
    [?] Objects, types, and names as bindings
    [?] Mutability and copying
    [?] Numbers and arithmetic
    [?] Strings and f-strings
    [?] Truthiness, None, and identity vs. equality

Control Flow and Iteration   [if locked: "(unlock: complete 3 Objects and Names skills)"]
    [?] Conditionals and guard clauses
    [?] for loops and the iteration protocol
    [?] while, break, continue, and loop else
    [?] Comprehensions
    [?] Structural pattern matching with match

Functions and Scope   [if locked: "(unlock: complete 3 Control Flow and Iteration skills)"]
    [?] Defining functions; functions as objects
    [?] Parameters and default values
    [?] *args, **kwargs, and unpacking calls
    [?] Scopes: LEGB, closures, and nonlocal
    [?] lambda and higher-order functions
    [?] Docstrings and annotations

Workhorse Containers   [if locked: "(unlock: complete 4 Functions and Scope skills)"]
    [?] Lists in practice
    [?] Tuples and unpacking
    [?] Dictionaries in practice
    [?] Sets and set operations

Classes and the Object Protocol   [if locked: "(unlock: complete 2 Workhorse Containers skills)"]
    [?] Classes, instances, and __init__
    [?] Methods and properties
    [?] Inheritance and super()
    [?] Dunder methods and the object protocol
    [?] Iterators from the object side

Robustness and Structure   [if locked: "(unlock: complete 3 Classes and the Object Protocol skills)"]
    [?] Handling exceptions
    [?] Raising and designing exceptions
    [?] Context managers and with
    [?] Generators and yield
    [?] Decorators
    [?] Modules, imports, and the __main__ guard
```

---

## Saved tree file template

```markdown
---
version: 3
topic: python
user: [git config user.name or "unknown"]
email: [git config user.email or "unknown"]
updated: [today's date YYYY-MM-DD]
level: [Explorer / Builder / Practitioner / Expert]
xp: [CURRENT_XP]
---

# Python Knowledge Graph

*[✓] Demonstrated · [~] Self-reported · [ ] Not yet · [★] Mastery target · [·] Locked*

## [ROOT] Objects and Names
- [STATUS|TYPE] Objects, types, and names as bindings
- [STATUS|TYPE] Mutability and copying
- [STATUS|TYPE] Numbers and arithmetic
- [STATUS|TYPE] Strings and f-strings
- [STATUS|TYPE] Truthiness, None, and identity vs. equality

## [A] Control Flow and Iteration
- [STATUS|TYPE] Conditionals and guard clauses
- [STATUS|TYPE] for loops and the iteration protocol
- [STATUS|TYPE] while, break, continue, and loop else
- [STATUS|TYPE] Comprehensions
- [STATUS|TYPE] Structural pattern matching with match

## [B] Functions and Scope
- [STATUS|TYPE] Defining functions; functions as objects
- [STATUS|TYPE] Parameters and default values
- [STATUS|TYPE] *args, **kwargs, and unpacking calls
- [STATUS|TYPE] Scopes: LEGB, closures, and nonlocal
- [STATUS|TYPE] lambda and higher-order functions
- [STATUS|TYPE] Docstrings and annotations

## [C] Workhorse Containers
- [STATUS|TYPE] Lists in practice
- [STATUS|TYPE] Tuples and unpacking
- [STATUS|TYPE] Dictionaries in practice
- [STATUS|TYPE] Sets and set operations

## [D] Classes and the Object Protocol
- [STATUS|TYPE] Classes, instances, and __init__
- [STATUS|TYPE] Methods and properties
- [STATUS|TYPE] Inheritance and super()
- [STATUS|TYPE] Dunder methods and the object protocol
- [STATUS|TYPE] Iterators from the object side

## [E] Robustness and Structure
- [STATUS|TYPE] Handling exceptions
- [STATUS|TYPE] Raising and designing exceptions
- [STATUS|TYPE] Context managers and with
- [STATUS|TYPE] Generators and yield
- [STATUS|TYPE] Decorators
- [STATUS|TYPE] Modules, imports, and the __main__ guard

## Frontier
- [frontier node name] — [criterion one-liner]

## Notes
<!-- Add personal notes here -->
```
