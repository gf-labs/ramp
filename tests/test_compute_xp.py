"""C1 regression lock.

``compute_xp`` reads each node's XP weight from the branch tier encoded in the
nearest ``## [SubTopic · TIER]`` header. Before the fix, the meta-topic saved
tree carried no tier in its headers, so the ``· TIER]`` regex never matched and
``compute_xp`` returned 0 for every real graph — silently zeroing the headline
XP/Level feature on every observer write. ``test_untiered_headers_return_zero``
pins that exact failure so it can never regress unnoticed.
"""

BRANCH = {"ROOT": 10, "A": 15, "B": 20, "C": 25, "D": 35, "E": 50}


def test_tiered_headers_sum_per_tier(observer):
    tree = (
        "## [Getting Started · ROOT] Core Foundations\n"
        "- [✓|exercise] a\n"
        "- [~|reported] b\n"
        "- [ ] c\n"
        "\n"
        "## [Build · A] Skills and Plugins\n"
        "- [✓|artifact] d\n"
    )
    # ROOT: 10 (✓) + 5 (~ floored) ; A: 15 (✓)  ->  30
    assert observer.compute_xp(tree) == 30


def test_every_tier_weight_counts(observer):
    tree = "".join(
        f"## [Topic · {tier}] section\n- [✓|artifact] node {tier}\n" for tier in BRANCH
    )
    assert observer.compute_xp(tree) == sum(BRANCH.values())  # 10+15+20+25+35+50 = 155


def test_reported_is_half_floored(observer):
    # D tier = 35 ; half, floored = 17
    assert observer.compute_xp("## [Build · D] x\n- [~|reported] y\n") == 17


def test_untiered_headers_return_zero(observer):
    # The pre-fix meta-topic format (no `· TIER`). This IS the C1 bug — pinned.
    tree = "## [Getting Started] Core Foundations\n- [✓|exercise] a\n"
    assert observer.compute_xp(tree) == 0


def test_not_yet_nodes_score_zero(observer):
    assert observer.compute_xp("## [Build · C] x\n- [ ] y\n- [ ] z\n") == 0


def test_compute_xp_duplicate_name_counts_once(core):
    # The B1 bug shape: one logical node misfiled under a second tier. The
    # first occurrence scores; the dupe adds 0 (validate_tree still flags it).
    tree = (
        "## [Build · C] Headless\n"
        "- [✓|historical] Headless Claude in CI/CD pipelines — r, 2026-06-01: n | next: 2026-06-02 [L1]\n"
        "\n"
        "## [Deployment · B] Patterns\n"
        "- [✓|historical] Headless Claude in CI/CD pipelines — r, 2026-06-01: n | next: 2026-06-02 [L1]\n"
    )
    assert core.compute_xp(tree) == 25  # C only — not 25 + 20


def test_compute_xp_duplicate_mixed_status_first_wins(core):
    tree = (
        "## [Build · A] One\n"
        "- [~|reported] Same node — r, 2026-06-01: claim\n"
        "## [Build · B] Two\n"
        "- [✓|exercise] Same node — r, 2026-06-01: n | next: 2026-06-02 [L1]\n"
    )
    assert core.compute_xp(tree) == 7  # A=15 halved+floored; the later [✓] dupe adds 0


def test_compute_xp_unnamed_lines_are_not_deduped(core):
    # Bullets with no parseable name can't be identified as duplicates — count both.
    tree = "## [Build · A] One\n- [✓|exercise]\n- [✓|exercise]\n"
    assert core.compute_xp(tree) == 30
