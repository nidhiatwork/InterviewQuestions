"""LeetCode #39 — Combination Sum  (Backtracking · Medium)

URL: https://leetcode.com/problems/combination-sum/

Problem
-------
Given an array of distinct integers `candidates` and a target integer
`target`, return a list of all unique combinations of candidates where
the chosen numbers sum to target. You may return the combinations in
any order.

The same number may be chosen from candidates an unlimited number of
times. Two combinations are unique if the frequency of at least one of
the chosen numbers is different.

Examples
--------
  candidates = [2,3,6,7], target = 7   ->  [[2,2,3], [7]]
  candidates = [2,3,5],   target = 8   ->  [[2,2,2,2], [2,3,3], [3,5]]
  candidates = [2],       target = 1   ->  []

Constraints
-----------
  1 <= candidates.length <= 30
  2 <= candidates[i] <= 40
  All elements of candidates are distinct.
  1 <= target <= 40

Run
---
  python 2026-06-02-combination-sum.py -v
"""

import unittest


class Solution:
    def combinationSum(self, candidates, target):
        raise NotImplementedError("Implement combinationSum")


# ----------------------------- helpers -----------------------------

def _canon(combos):
    """Normalize: sort each combo, then sort the outer list — for set comparison."""
    return sorted(sorted(c) for c in combos)


# ------------------------------ tests ------------------------------

class TestCombinationSum(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1(self):
        got = self.sol.combinationSum([2, 3, 6, 7], 7)
        self.assertEqual(_canon(got), _canon([[2, 2, 3], [7]]))

    def test_example_2(self):
        got = self.sol.combinationSum([2, 3, 5], 8)
        self.assertEqual(
            _canon(got),
            _canon([[2, 2, 2, 2], [2, 3, 3], [3, 5]]),
        )

    def test_example_3_impossible(self):
        self.assertEqual(self.sol.combinationSum([2], 1), [])

    def test_single_one_makes_anything(self):
        got = self.sol.combinationSum([1], 2)
        self.assertEqual(_canon(got), [[1, 1]])

    def test_single_candidate_equals_target(self):
        got = self.sol.combinationSum([1], 1)
        self.assertEqual(_canon(got), [[1]])

    def test_pick_just_the_target(self):
        got = self.sol.combinationSum([5, 4, 3], 4)
        self.assertEqual(_canon(got), [[4]])

    def test_unsorted_input(self):
        # Same problem as example 1 but candidates in scrambled order.
        got = self.sol.combinationSum([7, 3, 2, 6], 7)
        self.assertEqual(_canon(got), _canon([[2, 2, 3], [7]]))

    def test_target_smaller_than_all_candidates(self):
        self.assertEqual(self.sol.combinationSum([2, 3, 6, 7], 1), [])

    def test_multi_combo_unsorted(self):
        got = self.sol.combinationSum([8, 7, 4, 3], 11)
        self.assertEqual(_canon(got), _canon([[3, 4, 4], [3, 8], [4, 7]]))

    def test_no_duplicate_combos(self):
        # Easy to accidentally produce [2,3,3] AND [3,2,3] AND [3,3,2]
        # if recursion explores all orderings; canonical answer is just one.
        got = self.sol.combinationSum([2, 3, 5], 8)
        # Confirm uniqueness regardless of order:
        as_tuples = {tuple(sorted(c)) for c in got}
        self.assertEqual(len(as_tuples), len(got))


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  — peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
This is a classic "enumerate all combinations" problem — the standard
tool is recursive backtracking with a `start` index to suppress
duplicate orderings.

Mental model:
  - Walk the candidates left to right.
  - At each step you have a choice: either take candidates[i] (and
    stay at i because reuse is allowed) or skip it (advance to i+1).
  - Maintain `remaining = target - sum(picked_so_far)` and an
    in-progress `path`.
  - Base cases inside the recursion:
      * remaining == 0  -> path is a valid combination, snapshot it.
      * remaining <  0  -> dead end, prune.
      * i == len(c)     -> no more candidates, dead end.

The critical anti-duplicate trick is the `start` index. Without it,
[2,3,3] and [3,2,3] and [3,3,2] would all surface as "different"
recursion paths. By passing `i` (not `i+1`) when we *take* candidate i,
we allow reuse; by passing `start=i` when we recurse, we never revisit
earlier candidates — which forces every valid combination to appear in
non-decreasing index order, i.e. exactly once.

Pruning sort: if you sort candidates first, you can break out of the
loop as soon as `candidates[i] > remaining` instead of continuing to
explore obviously-too-big choices. Optional but cheap and noticeably
faster on adversarial inputs.

This is "decision-tree DFS with state passed down the call stack" — no
hash table needed, no memoization (paths are unique, so two paths can
never produce the same combination to dedupe against).

Complexity
----------
Let N = len(candidates), T = target, m = min(candidates).
- Time:  O(N^(T/m + 1))  — branching factor N, depth bounded by T/m
                            (worst case all-ones-ish). Very loose upper
                            bound; sort+prune brings it down a lot.
- Space: O(T/m)          — recursion depth + path; output not counted.

Python solution
---------------
class Solution:
    def combinationSum(self, candidates, target):
        candidates.sort()                 # enables the prune below
        results = []
        path = []

        def backtrack(start, remaining):
            if remaining == 0:
                results.append(path[:])   # snapshot — path mutates after
                return
            for i in range(start, len(candidates)):
                c = candidates[i]
                if c > remaining:         # sorted, so all later c's are too
                    break
                path.append(c)
                backtrack(i, remaining - c)   # i, not i+1 -> reuse allowed
                path.pop()

        backtrack(0, target)
        return results

Interview tips
--------------
- Open by saying "this is decision-tree DFS — at each candidate I either
  take it (and stay) or skip it (and advance)." That single sentence
  earns you the framing-points; the code is just plumbing.
- The interviewer will absolutely probe "why pass `i` instead of `i+1`?"
  Answer crisply: "i+1 would forbid reuse, which the problem allows; `i`
  is the take-with-reuse branch, `start=i+1` would be the skip branch
  but the for-loop's next iteration already advances past i implicitly."
- They'll also probe "how do you avoid duplicate combinations?" Answer:
  "I enforce non-decreasing index order via `start`. Every distinct
  multiset surfaces exactly once because there's only one way to list
  it with indices in non-decreasing order."
- `path[:]` snapshot is load-bearing. A junior trap is appending `path`
  itself and getting `[[]] * k` at the end because every entry is the
  same mutating list. Mention this explicitly — interviewers love it.
- Pruning: sort upfront, break when `c > remaining`. Trivial change,
  noticeable speedup. They'll often ask "can you make this faster?"
  and this is the cheap win.
- Related problems they may pivot to:
    * #40 Combination Sum II  — duplicates in input, can't reuse a
      single element. Same skeleton, but `start=i+1` on the recurse
      call AND `if i > start and candidates[i] == candidates[i-1]:
      continue` to skip equal siblings at the same recursion depth.
    * #216 Combination Sum III — pick exactly k distinct numbers from
      1..9. Same skeleton, add `len(path) == k` check at the base case.
    * #377 Combination Sum IV — "count" instead of "list." Order
      matters and only the count is needed; the right tool there is
      iterative tabulation (count[t] = sum of count[t-c] over coins),
      not recursive enumeration.
- Sanity-check yourself by computing one branch on paper for
  candidates=[2,3,6,7], target=7: start=0 take 2 (rem=5), take 2
  (rem=3), take 2 (rem=1), no candidate fits -> back; take 3 (rem=0)
  -> [2,2,3]. Then unwind, etc. Walking one branch verbally for ~30s
  shows the interviewer you actually traced your own logic.
"""
