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
