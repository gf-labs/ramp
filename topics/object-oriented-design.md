---
topic: object-oriented-design
node_count: 29
version: 1
source_url: http://scg.unibe.ch/download/oorp/
goal: ramp them up on object-oriented design — how to turn a requirement into objects with clear responsibilities, choose relationships that absorb change rather than resist it, and recognize and repair design that has gone wrong
description: Object-oriented design — responsibilities and encapsulation, turning requirements into a model with CRC cards, structural relationships, designing for change, patterns as vocabulary, and repairing design that has decayed.
---

# Object-Oriented Design Knowledge Graph Schema

This file defines the curriculum for the `object-oriented-design` topic: designing
software out of objects that hold responsibilities, and judging whether a design will
survive the next requirement.

**On sources.** A design discipline has no reference manual the way Git has Pro Git or
Bash has the GNU manual — it has canonical literature. This topic is therefore grounded
in a named source set rather than a single spine, which is a deliberate deviation from
`git`/`bash`/`python`:

- **[Object-Oriented Reengineering Patterns](http://scg.unibe.ch/download/oorp/)** (Demeyer,
  Ducasse, Nierstrasz) — the declared canonical source. Out of print from Morgan Kaufmann,
  rights reverted to the authors, now **CC-BY-SA 4.0**. Grounds scenario-driven model
  validation and the repair branch.
- **[Responsibility-Driven Design](https://www.wirfs-brock.com/resp_driven_design.html)**
  (Rebecca Wirfs-Brock) — the canonical method for going from a requirement to objects.
  She originated both RDD and CRC cards. Grounds Branch A.
- **[Game Programming Patterns](https://gameprogrammingpatterns.com/)** (Robert Nystrom) —
  a complete free web book that revisits the classic patterns with unusually honest
  cost/benefit discussion. Grounds Branch D. Its examples are game-flavored; the design
  content is not.
- **[refactoring.com/catalog](https://refactoring.com/catalog/)** and
  **[martinfowler.com](https://martinfowler.com/)** (Martin Fowler) — the smell-to-repair
  vocabulary and per-concept essays.
- **[Design Principles and Design Patterns](https://staff.cs.utu.fi/~jounsmed/doos_06/material/DesignPrinciplesAndPatterns.pdf)**
  (Robert C. Martin, 2000) — cited only where the SOLID names originate. The paper's
  original host is gone and this is a course mirror, so it is deliberately limited to two
  nodes; every other node rests on a source with a durable home.

**Scope.** Design at the level of objects, their responsibilities, and their
relationships. Deliberately **out of scope**: domain modelling in the DDD sense —
aggregates, bounded contexts, ubiquitous language (a future sibling topic,
`domain-modeling`); data structures and algorithmic complexity (a future sibling,
`data-structures-algorithms`); language-specific object mechanics such as Python's
descriptors and dunder protocol (`python` Branch D); system-scale architecture
(microservices, hexagonal, event-driven); UML notation as an artifact; and functional
design. 29 nodes across 6 branches, foundations-first with each branch unlocking the next.

---

## Node definitions

29 nodes across 6 branches.

### [ROOT] Objects and responsibilities (always unlocked — 5 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|-----------|-----|
| What an object is: behavior over data | Can explain an object as a participant defined by what it *does* rather than what it holds, and can name what goes wrong when classes become field-bags with the logic living elsewhere — including where that behavior should have gone | Qualitative | class_definitions > 0 → `[~\|artifact]` | https://martinfowler.com/bliki/AnemicDomainModel.html | object-oriented-design-what-an-object-is-behavior-over-data |
| Responsibilities: doing, knowing, deciding | Can classify what an object is responsible for — doing work, knowing information, or deciding — and can assign a new requirement's responsibility to a specific object with a stated reason, distinguishing knowing from doing | Qualitative | None | https://www.wirfs-brock.com/PDFs/Responsibility-Driven.pdf | object-oriented-design-responsibilities-doing-knowing-deciding |
| Encapsulation and information hiding | Can name a change that stays local *because* of what a class hides, and can explain why private fields wrapped in public accessors is not information hiding | Qualitative | None | https://refactoring.com/catalog/encapsulateRecord.html | object-oriented-design-encapsulation-and-information-hiding |
| Tell, don't ask | Can rewrite a fragment that pulls data out of an object in order to decide, into one that asks the object to decide — and can say when asking is legitimate rather than a smell | Exercise / Qualitative | None | https://martinfowler.com/bliki/TellDontAsk.html | object-oriented-design-tell-don-t-ask |
| Command-query separation | Can explain why a method should either change state or answer a question but not both, and can name a concrete surprise caused by violating it | Qualitative | None | https://martinfowler.com/bliki/CommandQuerySeparation.html | object-oriented-design-command-query-separation |

### [A] From requirements to a model (5 nodes, unlocks when ROOT ≥ 3 `[✓]`)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|-----------|-----|
| Finding candidate objects in a problem statement | Given a written requirement, can extract candidate objects and defend why a particular noun did *not* become a class — because it was an attribute, an event, or a role | Exercise / Qualitative | None | https://www.wirfs-brock.com/PDFs/Responsibility-Driven.pdf | object-oriented-design-finding-candidate-objects-in-a-problem-statement |
| CRC cards: class, responsibility, collaborator | Has modelled a small system with CRC cards, and can explain what the collaborator column captures that a class diagram does not | Exercise / Artifact | None | https://www.wirfs-brock.com/PDFs/A%20Brief%20Tour%20of%20RDD%20in%202004.pdf | object-oriented-design-crc-cards-class-responsibility-collaborator |
| Assigning a responsibility to the right object | Given a behavior, can choose which object should own it and justify the choice against a named rejected alternative — on information ownership or resulting coupling, not convenience | Qualitative | None | https://www.wirfs-brock.com/resp_driven_design.html | object-oriented-design-assigning-a-responsibility-to-the-right-object |
| Role stereotypes | Can name the role an object plays — information holder, structurer, service provider, coordinator, controller, interfacer — and use that stereotype to reject a responsibility that does not belong to it | Qualitative | None | https://www.wirfs-brock.com/PDFs/A%20Brief%20Tour%20of%20RDD%20in%202004.pdf | object-oriented-design-role-stereotypes |
| Walking a scenario to validate a model | Can take a use-case scenario, trace the message flow across the objects, and find a defect that way — a missing responsibility, or an object that turns out to do nothing | Exercise / Qualitative | None | http://scg.unibe.ch/download/oorp/OORP.pdf | object-oriented-design-walking-a-scenario-to-validate-a-model |

### [B] Structure and relationships (5 nodes, unlocks when Branch A ≥ 3 `[✓]`)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|-----------|-----|
| Composition over inheritance | Can state what inheritance couples that delegation does not, and has converted an inheritance relationship into composition — naming the fragile-base-class or leaked-behavior failure it avoided | Exercise / Qualitative | None | https://refactoring.com/catalog/replaceSuperclassWithDelegate.html | object-oriented-design-composition-over-inheritance |
| Substitutability: when inheritance is right | Can state the substitutability test — a subtype must work wherever the supertype does, without the caller knowing — and can give an example that passes the English "is-a" reading but fails the test | Qualitative | subclass_declarations > 0 → `[~\|artifact]` | https://staff.cs.utu.fi/~jounsmed/doos_06/material/DesignPrinciplesAndPatterns.pdf | object-oriented-design-substitutability-when-inheritance-is-right |
| Coupling: naming it and reducing it | Can identify what couples two classes, name the kind of coupling, and describe one concrete change that reduces it — while rejecting indirection added for its own sake | Qualitative | None | https://martinfowler.com/ieeeSoftware/coupling.pdf | object-oriented-design-coupling-naming-it-and-reducing-it |
| Cohesion: one class, one job | Can explain why a class with two unrelated reasons to change is a problem, and has split one along its actual seam rather than by size | Exercise / Qualitative | None | https://refactoring.com/catalog/extractClass.html | object-oriented-design-cohesion-one-class-one-job |
| Law of Demeter and train-wreck chains | Can spot a chained call that reaches through one object to get at another, explain what knowledge the chain leaks, and fix it by moving behavior rather than adding a wrapper | Exercise / Qualitative | None | https://refactoring.com/catalog/hideDelegate.html | object-oriented-design-law-of-demeter-and-train-wreck-chains |

### [C] Designing for change (5 nodes, unlocks when Branch B ≥ 3 `[✓]`)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|-----------|-----|
| Open-closed: extending without editing | Can describe a change that was absorbed by adding a class rather than editing existing ones, and can name the abstraction that made that possible | Qualitative / Historical | None | https://staff.cs.utu.fi/~jounsmed/doos_06/material/DesignPrinciplesAndPatterns.pdf | object-oriented-design-open-closed-extending-without-editing |
| Dependency inversion and injection | Can explain why a high-level policy should not depend on a low-level detail, has inverted such a dependency behind an abstraction, and distinguishes the principle from any particular DI framework | Exercise / Qualitative | interface_declarations > 0 → `[~\|artifact]` | https://martinfowler.com/articles/injection.html | object-oriented-design-dependency-inversion-and-injection |
| Single responsibility as one reason to change | Can restate single-responsibility in terms of *who* asks for the change, and apply it to split — or deliberately decline to split — a class, without appealing to line count | Qualitative | None | https://blog.cleancoder.com/uncle-bob/2020/10/18/Solid-Relevance.html | object-oriented-design-single-responsibility-as-one-reason-to-change |
| Replacing conditionals with polymorphism | Has replaced a type switch or conditional chain with polymorphic dispatch, and can name a case where the conditional should have been left alone | Exercise | None | https://refactoring.com/catalog/replaceConditionalWithPolymorphism.html | object-oriented-design-replacing-conditionals-with-polymorphism |
| Speculative generality and YAGNI | Can explain why building for an unrequested future usually costs more than it saves, and can name an abstraction they removed or declined — while distinguishing YAGNI from never abstracting | Qualitative / Historical | None | https://martinfowler.com/bliki/Yagni.html | object-oriented-design-speculative-generality-and-yagni |

### [D] Patterns as design vocabulary (5 nodes, unlocks when Branch C ≥ 3 `[✓]`)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|-----------|-----|
| State: modelling modes as objects | Can replace a flag-or-enum state machine with state objects, and can say what that buys and what it costs in indirection | Exercise / Qualitative | None | https://gameprogrammingpatterns.com/state.html | object-oriented-design-state-modelling-modes-as-objects |
| Observer: decoupling a notifier from listeners | Can explain precisely what Observer decouples, and can name one of its classic hazards — listener lifetime and leaks, or undefined notification ordering | Qualitative | None | https://gameprogrammingpatterns.com/observer.html | object-oriented-design-observer-decoupling-a-notifier-from-listeners |
| Command: turning a request into an object | Can explain what reifying a request as an object enables — undo, queueing, replay, logging — and has used it for at least one of those | Exercise / Qualitative | None | https://gameprogrammingpatterns.com/command.html | object-oriented-design-command-turning-a-request-into-an-object |
| Components over deep hierarchies | Can explain how composing an object from components replaces a deep inheritance tree, and when that indirection is not worth paying for | Qualitative | None | https://gameprogrammingpatterns.com/component.html | object-oriented-design-components-over-deep-hierarchies |
| Knowing when a pattern is the wrong answer | Can name a pattern they applied and later removed, or declined to apply, and articulate why — treating patterns as shared vocabulary rather than as design goals | Qualitative / Historical | None | https://gameprogrammingpatterns.com/architecture-performance-and-games.html | object-oriented-design-knowing-when-a-pattern-is-the-wrong-answer |

### [E] Recognizing and repairing bad design (4 nodes, unlocks when Branch D ≥ 3 `[✓]`)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|-----------|-----|
| Reading smells as design signals | Can name three code smells and, for each, the *design* defect it points at — not merely the syntactic pattern that identifies it | Qualitative | None | https://martinfowler.com/bliki/CodeSmell.html | object-oriented-design-reading-smells-as-design-signals |
| God class and data class as one problem | Can recognize an over-large class and a behavior-free data class as two halves of the same misplaced responsibility, and describe the redistribution that fixes both | Qualitative | None | http://scg.unibe.ch/download/oorp/OORP.pdf | object-oriented-design-god-class-and-data-class-as-one-problem |
| Refactoring toward responsibilities in safe steps | Has moved behavior between classes in small steps backed by tests or the compiler, and can explain why the step size and ordering matter rather than doing it in one edit | Exercise / Historical | refactor_commits > 0 → `[~\|historical]` | https://refactoring.com/catalog/moveFunction.html | object-oriented-design-refactoring-toward-responsibilities-in-safe-steps |
| Design as an investment in change | Can argue when improving a design pays for itself and when it does not, in terms of how often the code is expected to change rather than how it looks | Qualitative | None | https://martinfowler.com/bliki/DesignStaminaHypothesis.html | object-oriented-design-design-as-an-investment-in-change |

---

## Probes

| name | primitive | args |
|------|-----------|------|
| class_definitions      | grep-count   | "^ *class " src lib app tests scripts |
| interface_declarations | grep-count   | "^ *(interface\|protocol) " src lib app tests scripts |
| abstract_types         | grep-count   | "@abstractmethod\|ABCMeta\|abstract class" src lib app tests scripts |
| subclass_declarations  | grep-count   | "^ *class [A-Za-z_][A-Za-z0-9_]*\(" src lib app tests scripts |
| refactor_commits       | git-log-grep | ^refactor |
| unit_tests             | glob-count   | **/test_*.py --exclude venv/** |

Notes: all five `grep-count`/`glob-count` probes scope to the conventional source roots (`src lib app tests scripts`) rather than the whole tree, so vendored and virtual-environment code never counts; a missing path contributes 0, which biases toward precision — an under-firing signal costs only a seed, while a false positive corrupts the graph. `subclass_declarations` matches a class header followed by an open parenthesis, which in Python is a base-class list; the `\(` is a literal parenthesis, not a group. `interface_declarations` and `abstract_types` catch the explicit-abstraction idioms of several languages, so both are best-effort rather than exhaustive. `refactor_commits` counts commits whose message begins with `refactor`, which witnesses the user's own history in this repository. Every signal below seeds `[~]`, never `[✓]` — see the direct-witness note under *Detection signals*.

---

## Detection signals

| Collected evidence | Node → status |
|--------------------|---------------|
| class_definitions > 0 | ROOT: "What an object is: behavior over data" → `[~\|artifact]` |
| subclass_declarations > 0 | B: "Substitutability: when inheritance is right" → `[~\|artifact]` |
| abstract_types > 0 | B: "Substitutability: when inheritance is right" → `[~\|artifact]` |
| interface_declarations > 0 | C: "Dependency inversion and injection" → `[~\|artifact]` |
| refactor_commits > 0 | E: "Refactoring toward responsibilities in safe steps" → `[~\|historical]` |
| unit_tests > 0 | E: "Refactoring toward responsibilities in safe steps" → `[~\|artifact]` |

Every signal seeds `[~]`, never `[✓]`: this is a design topic, and the presence of classes, abstractions, or a refactor commit is *consistent with* holding the skill without directly witnessing the judgment behind it (the direct-witness rule). A class hierarchy proves someone wrote a hierarchy, not that they could defend it — teach-back verification is what upgrades these.

---

## Gap questions

| Branch | Gap | Ask this |
|--------|-----|----------|
| [ROOT] | Behavior over data | "You open a class that's nothing but fields with getters and setters, and the logic that uses it lives in a service elsewhere. What's wrong with that, and where should the behavior have gone?" |
| [ROOT] | Responsibilities | "A new requirement lands: orders over a threshold get a discount. Which object should own that decision, and why that one rather than the caller?" |
| [ROOT] | Encapsulation | "If a class makes every field private but exposes a getter and setter for each, is it encapsulated? Explain what information hiding actually buys you." |
| [ROOT] | Tell, don't ask | "Here's a fragment: `if (account.getBalance() < amount) { reject(); }`. Rewrite it in the tell-don't-ask style and explain what moved. When would asking be fine?" |
| [ROOT] | Command-query separation | "Why is a method that both saves a record and returns whether it's valid a problem? Give a concrete way that bites someone." |
| [A] | Candidate objects | "Given a one-paragraph description of a parking garage, how do you get from that text to a set of classes? Name one noun in it that should *not* become a class, and say why." |
| [A] | CRC cards | "Walk me through modelling something small with CRC cards. What does the collaborator column tell you that a class diagram doesn't?" |
| [A] | Assigning responsibility | "Two objects could plausibly own the same behavior. How do you decide? Talk me through a case where you picked one and what made the other worse." |
| [A] | Role stereotypes | "What kind of object is it — does it hold information, coordinate others, provide a service, or talk to the outside world? Give an example of using that answer to reject a responsibility someone wanted to put on it." |
| [A] | Scenario walking | "You've drafted a model. How do you check it before writing code? Describe a time walking through a scenario exposed something missing." |
| [B] | Composition over inheritance | "You inherit from a base class to reuse one method. What does that cost you, and what would you do instead? What specifically breaks later?" |
| [B] | Substitutability | "Give me an example of something that reads as 'is-a' in English but shouldn't be a subclass. What's the test that catches it?" |
| [B] | Coupling | "Two classes are too tangled to change independently. How do you describe the coupling precisely, and what's one change that reduces it without just adding an interface?" |
| [B] | Cohesion | "A class has grown to 800 lines. How do you decide where to split it — or whether to split it at all?" |
| [B] | Law of Demeter | "You see `order.getCustomer().getAddress().getCity()`. What does that chain tell you about the design, and how do you fix it?" |
| [C] | Open-closed | "Describe a change you absorbed by adding a new class instead of editing existing ones. What was already in place that let you do that?" |
| [C] | Dependency inversion | "Your business logic needs to send email. How do you keep the logic from depending on the mail library? And is that the same thing as using a DI framework?" |
| [C] | Single responsibility | "What does 'one reason to change' actually mean? Apply it to a class you've worked on — and tell me about a time you decided *not* to split." |
| [C] | Conditionals to polymorphism | "You have a switch on a type code appearing in four places. Walk me through replacing it with polymorphism — and tell me when you'd leave the switch alone." |
| [C] | YAGNI | "Tell me about an abstraction you built for a future that never arrived, or one you deliberately didn't build. How do you tell that apart from just never abstracting?" |
| [D] | State pattern | "You have an object with an `isLoading` / `isReady` / `isFailed` set of flags. How would you model that with state objects, and what does it cost?" |
| [D] | Observer | "What does Observer actually decouple? Name a way it goes wrong in practice." |
| [D] | Command | "What do you get by turning a request into an object? Give a concrete feature that becomes easy afterwards." |
| [D] | Components | "How does composing an object out of components differ from a deep inheritance tree? When is the extra indirection not worth it?" |
| [D] | Patterns misapplied | "Tell me about a pattern you applied and later took out, or one you decided against. What made it the wrong call?" |
| [E] | Smells | "Name three code smells and, for each, the design problem it's actually pointing at — not just how you spot it." |
| [E] | God class / data class | "A codebase has one enormous manager class and a pile of classes that are pure data. How are those two things related, and what's the fix?" |
| [E] | Safe refactoring | "You need to move behavior from one class to another in code that ships. Walk me through your sequence — and what keeps you safe between steps." |
| [E] | Design as investment | "When is cleaning up a design *not* worth doing? What decides it for you?" |

### Qualitative rubric

- **`[✓]` Demonstrated**: Contains at least one specific, verifiable detail — a concrete refactoring performed, a named tradeoff navigated, a rejected alternative with a reason, or a causal explanation of *why*, not just *what*.
- **`[~]` Self-reported**: Affirmative but vague. "Yeah, I use composition over inheritance" with no mechanism, no scenario, no cost named.
- **`[ ]` Not yet**: Negative, "not sure," or "heard of it but haven't done it."

### Answer → node mapping

| Answer contains | Node → status |
|-----------------|---------------|
| Names the anemic/field-bag failure and where the behavior belongs | ROOT: "What an object is: behavior over data" → `[✓\|reported]` |
| Assigns the decision to a specific object with a reason, distinguishing knowing from doing | ROOT: "Responsibilities: doing, knowing, deciding" → `[✓\|reported]` |
| Rejects getter/setter pairs as encapsulation; names a change kept local by hiding | ROOT: "Encapsulation and information hiding" → `[✓\|reported]` |
| Rewrites the fragment to ask the object to decide, and bounds when asking is fine | ROOT: "Tell, don't ask" → `[✓\|reported]` |
| States the separation and gives a concrete surprise from violating it | ROOT: "Command-query separation" → `[✓\|reported]` |
| Extracts candidates from prose and rejects a noun as attribute, event, or role | A: "Finding candidate objects in a problem statement" → `[✓\|reported]` |
| Describes real CRC modelling and what collaborators capture beyond a diagram | A: "CRC cards: class, responsibility, collaborator" → `[✓\|reported]` |
| Chooses an owner and names the rejected alternative with the reason | A: "Assigning a responsibility to the right object" → `[✓\|reported]` |
| Names a stereotype and uses it to reject a misplaced responsibility | A: "Role stereotypes" → `[✓\|reported]` |
| Describes tracing a scenario through objects and the defect it exposed | A: "Walking a scenario to validate a model" → `[✓\|reported]` |
| Names what inheritance couples and describes converting it to delegation | B: "Composition over inheritance" → `[✓\|reported]` |
| States the substitutability test and gives an is-a example that fails it | B: "Substitutability: when inheritance is right" → `[✓\|reported]` |
| Names the kind of coupling and a concrete reduction that isn't bare indirection | B: "Coupling: naming it and reducing it" → `[✓\|reported]` |
| Identifies the seam rather than the size when splitting a class | B: "Cohesion: one class, one job" → `[✓\|reported]` |
| Reads the chain as leaked knowledge and fixes by moving behavior | B: "Law of Demeter and train-wreck chains" → `[✓\|reported]` |
| Describes a change absorbed by addition and names the enabling abstraction | C: "Open-closed: extending without editing" → `[✓\|reported]` |
| Inverts the dependency behind an abstraction and separates it from a framework | C: "Dependency inversion and injection" → `[✓\|reported]` |
| Ties one reason to change to an actor, including a decision not to split | C: "Single responsibility as one reason to change" → `[✓\|reported]` |
| Describes a real switch-to-polymorphism conversion plus when to leave it | C: "Replacing conditionals with polymorphism" → `[✓\|reported]` |
| Names an abstraction removed or declined, distinguished from never abstracting | C: "Speculative generality and YAGNI" → `[✓\|reported]` |
| Converts flags to state objects and names the indirection cost | D: "State: modelling modes as objects" → `[✓\|reported]` |
| States what Observer decouples plus a lifetime or ordering hazard | D: "Observer: decoupling a notifier from listeners" → `[✓\|reported]` |
| Names what reifying a request enables and a feature built on it | D: "Command: turning a request into an object" → `[✓\|reported]` |
| Contrasts components with a deep hierarchy and bounds when it's overkill | D: "Components over deep hierarchies" → `[✓\|reported]` |
| Names a pattern applied and removed, or declined, with the reasoning | D: "Knowing when a pattern is the wrong answer" → `[✓\|reported]` |
| Maps three smells to the design defects behind them | E: "Reading smells as design signals" → `[✓\|reported]` |
| Links the god class and the data class as one misplacement plus the redistribution | E: "God class and data class as one problem" → `[✓\|reported]` |
| Describes a stepwise move with the safety mechanism between steps | E: "Refactoring toward responsibilities in safe steps" → `[✓\|reported]` |
| Argues the payoff in terms of expected change rate, not aesthetics | E: "Design as an investment in change" → `[✓\|reported]` |

---

## Unlock thresholds

- Branch A unlocks when ROOT ≥ 3 `[✓]`
- Branch B unlocks when Branch A ≥ 3 `[✓]`
- Branch C unlocks when Branch B ≥ 3 `[✓]`
- Branch D unlocks when Branch C ≥ 3 `[✓]`
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
Objects and Responsibilities
    [?] What an object is: behavior over data
    [?] Responsibilities: doing, knowing, deciding
    [?] Encapsulation and information hiding
    [?] Tell, don't ask
    [?] Command-query separation

From Requirements to a Model   [if locked: "(unlock: complete 3 Objects and Responsibilities skills)"]
    [?] Finding candidate objects in a problem statement
    [?] CRC cards: class, responsibility, collaborator
    [?] Assigning a responsibility to the right object
    [?] Role stereotypes
    [?] Walking a scenario to validate a model

Structure and Relationships   [if locked: "(unlock: complete 3 From Requirements to a Model skills)"]
    [?] Composition over inheritance
    [?] Substitutability: when inheritance is right
    [?] Coupling: naming it and reducing it
    [?] Cohesion: one class, one job
    [?] Law of Demeter and train-wreck chains

Designing for Change   [if locked: "(unlock: complete 3 Structure and Relationships skills)"]
    [?] Open-closed: extending without editing
    [?] Dependency inversion and injection
    [?] Single responsibility as one reason to change
    [?] Replacing conditionals with polymorphism
    [?] Speculative generality and YAGNI

Patterns as Design Vocabulary   [if locked: "(unlock: complete 3 Designing for Change skills)"]
    [?] State: modelling modes as objects
    [?] Observer: decoupling a notifier from listeners
    [?] Command: turning a request into an object
    [?] Components over deep hierarchies
    [?] Knowing when a pattern is the wrong answer

Recognizing and Repairing Bad Design   [if locked: "(unlock: complete 3 Patterns as Design Vocabulary skills)"]
    [?] Reading smells as design signals
    [?] God class and data class as one problem
    [?] Refactoring toward responsibilities in safe steps
    [?] Design as an investment in change
```

---

## Saved tree file template

```markdown
---
version: 3
topic: object-oriented-design
user: [git config user.name or "unknown"]
email: [git config user.email or "unknown"]
updated: [today's date YYYY-MM-DD]
level: [Explorer / Builder / Practitioner / Expert]
xp: [CURRENT_XP]
---

# Object-Oriented Design Knowledge Graph

*[✓] Demonstrated · [~] Self-reported · [ ] Not yet · [★] Mastery target · [·] Locked*

## [ROOT] Objects and Responsibilities
- [STATUS|TYPE] What an object is: behavior over data
- [STATUS|TYPE] Responsibilities: doing, knowing, deciding
- [STATUS|TYPE] Encapsulation and information hiding
- [STATUS|TYPE] Tell, don't ask
- [STATUS|TYPE] Command-query separation

## [A] From Requirements to a Model
- [STATUS|TYPE] Finding candidate objects in a problem statement
- [STATUS|TYPE] CRC cards: class, responsibility, collaborator
- [STATUS|TYPE] Assigning a responsibility to the right object
- [STATUS|TYPE] Role stereotypes
- [STATUS|TYPE] Walking a scenario to validate a model

## [B] Structure and Relationships
- [STATUS|TYPE] Composition over inheritance
- [STATUS|TYPE] Substitutability: when inheritance is right
- [STATUS|TYPE] Coupling: naming it and reducing it
- [STATUS|TYPE] Cohesion: one class, one job
- [STATUS|TYPE] Law of Demeter and train-wreck chains

## [C] Designing for Change
- [STATUS|TYPE] Open-closed: extending without editing
- [STATUS|TYPE] Dependency inversion and injection
- [STATUS|TYPE] Single responsibility as one reason to change
- [STATUS|TYPE] Replacing conditionals with polymorphism
- [STATUS|TYPE] Speculative generality and YAGNI

## [D] Patterns as Design Vocabulary
- [STATUS|TYPE] State: modelling modes as objects
- [STATUS|TYPE] Observer: decoupling a notifier from listeners
- [STATUS|TYPE] Command: turning a request into an object
- [STATUS|TYPE] Components over deep hierarchies
- [STATUS|TYPE] Knowing when a pattern is the wrong answer

## [E] Recognizing and Repairing Bad Design
- [STATUS|TYPE] Reading smells as design signals
- [STATUS|TYPE] God class and data class as one problem
- [STATUS|TYPE] Refactoring toward responsibilities in safe steps
- [STATUS|TYPE] Design as an investment in change

## Frontier
- [frontier node name] — [criterion one-liner]

## Notes
<!-- Add personal notes here -->
```
