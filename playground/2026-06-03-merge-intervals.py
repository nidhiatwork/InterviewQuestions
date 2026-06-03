"""LeetCode #56 — Merge Intervals  (Array · Medium)

URL: https://leetcode.com/problems/merge-intervals/

Problem
-------
Given an array of intervals where intervals[i] = [start_i, end_i],
merge all overlapping intervals and return an array of the
non-overlapping intervals that cover all the intervals in the input.

Two intervals [a, b] and [c, d] are considered overlapping if they
share at least one point — i.e. they touch (b == c) or properly
overlap (b > c).

Examples
--------
  intervals = [[1,3],[2,6],[8,10],[15,18]]   -> [[1,6],[8,10],[15,18]]
  intervals = [[1,4],[4,5]]                  -> [[1,5]]
  intervals = [[1,4],[0,4]]                  -> [[0,4]]
  intervals = [[1,4],[2,3]]                  -> [[1,4]]   (full containment)

Constraints
-----------
  1 <= intervals.length <= 10^4
  intervals[i].length == 2
  0 <= start_i <= end_i <= 10^4

Run
---
  python 2026-06-03-merge-intervals.py -v
"""

import unittest


class Solution:
    def merge(self, intervals):
        raise NotImplementedError("Implement merge")


# ----------------------------- helpers -----------------------------

def _canon(result):
    """Normalize a result so test comparisons are order-independent."""
    return sorted([list(iv) for iv in result])


# ------------------------------ tests ------------------------------

class TestMergeIntervals(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1(self):
        got = self.sol.merge([[1, 3], [2, 6], [8, 10], [15, 18]])
        self.assertEqual(_canon(got), _canon([[1, 6], [8, 10], [15, 18]]))

    def test_example_2_touching(self):
        # [1,4] and [4,5] share the point 4 -> must merge.
        got = self.sol.merge([[1, 4], [4, 5]])
        self.assertEqual(_canon(got), [[1, 5]])

    def test_unsorted_input(self):
        got = self.sol.merge([[15, 18], [8, 10], [2, 6], [1, 3]])
        self.assertEqual(_canon(got), _canon([[1, 6], [8, 10], [15, 18]]))

    def test_full_containment(self):
        # [2,3] is entirely inside [1,4]; result must keep [1,4].
        got = self.sol.merge([[1, 4], [2, 3]])
        self.assertEqual(_canon(got), [[1, 4]])

    def test_single_interval(self):
        self.assertEqual(self.sol.merge([[5, 7]]), [[5, 7]])

    def test_zero_width_intervals(self):
        # Endpoints can be equal (start == end), and identical intervals merge.
        got = self.sol.merge([[1, 1], [1, 1], [2, 2]])
        self.assertEqual(_canon(got), [[1, 1], [2, 2]])

    def test_all_overlap_into_one(self):
        got = self.sol.merge([[1, 10], [2, 3], [4, 8], [9, 9]])
        self.assertEqual(_canon(got), [[1, 10]])

    def test_no_overlap_at_all(self):
        got = self.sol.merge([[1, 2], [3, 4], [5, 6]])
        self.assertEqual(_canon(got), [[1, 2], [3, 4], [5, 6]])

    def test_gap_of_exactly_one(self):
        # [1,2] and [3,4] do NOT touch -> stay separate.
        got = self.sol.merge([[1, 2], [3, 4]])
        self.assertEqual(_canon(got), [[1, 2], [3, 4]])

    def test_chain_merge(self):
        # Each pair barely touches: 1-3, 3-5, 5-7, 7-9 -> one big [1,9].
        got = self.sol.merge([[1, 3], [3, 5], [5, 7], [7, 9]])
        self.assertEqual(_canon(got), [[1, 9]])

    def test_starts_equal_ends_differ(self):
        # Same start, varying end -> all merge into [0, max_end].
        got = self.sol.merge([[0, 2], [0, 5], [0, 1]])
        self.assertEqual(_canon(got), [[0, 5]])


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  — peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
The cleanest framing is "sort by start, then sweep left to right and
glue together whatever touches."

Why sorting works: once intervals are sorted by their start, the only
interval that can overlap with the current "in-flight" merged interval
is the next one in line. Any interval that comes later starts even
further right and either touches/overlaps with what we're holding
(then we extend it) or starts past its end (then we ship the held
interval and start a new one). This is a classic single-pass sweep
after sort.

Algorithm (sweep-after-sort):
  1. Sort intervals by start.
  2. Walk left to right with a single "in-flight" interval that we
     keep extending while the next interval's start is <= its end.
  3. The instant the next interval starts strictly past our held end,
     ship the held interval and adopt the next one as the new held one.
  4. After the loop, ship whatever's still in hand.

The touching rule (b == c counts as overlap) is captured by `<=`,
not `<`. Watch that — `<` would split [1,4] and [4,5].

Two implementation tactics, both O(n log n) total:

  (a) Build the answer list and either extend its last entry's end
      (`out[-1][1] = max(out[-1][1], end)`) or append a fresh entry.
      Lean, no separate "in-flight" variable.

  (b) Keep an explicit `(cur_start, cur_end)` pair, append it when
      you can't extend any more. Reads slightly more like a state
      machine, useful if the interviewer asks "now stream the input
      one interval at a time" — at which point you also need the
      input pre-sorted by the producer for the streaming variant to
      be correct.

The `max(out[-1][1], new_end)` is load-bearing: without `max`, the
full-containment case ([1,4] then [2,3]) would shrink the held end
from 4 down to 3, which is wrong.

Complexity
----------
- Time:  O(n log n)  — dominated by the sort; the sweep is O(n).
- Space: O(n)        — output list (or O(log n) for the sort's stack
                        if you sort in place and don't count output).

Python solution
---------------
class Solution:
    def merge(self, intervals):
        intervals.sort(key=lambda iv: iv[0])
        out = []
        for s, e in intervals:
            if out and s <= out[-1][1]:           # touches or overlaps
                out[-1][1] = max(out[-1][1], e)   # max -> handles containment
            else:
                out.append([s, e])
        return out

Interview tips
--------------
- Open with the one-liner that sells the whole algorithm: "sort by
  start, then sweep — at every step you're either extending the
  in-flight interval or shipping it and starting a new one." That's
  the entire idea; the code is plumbing.
- The two traps interviewers love to spring:
    (1) Touching counts as overlap. Use `<=`, not `<`. Say it out
        loud: "the problem treats [1,4] and [4,5] as overlapping
        because they share the point 4."
    (2) Full containment ([1,4] then [2,3]) — without `max(end,
        new_end)` you'd accidentally shrink the held end. Mention
        you used `max` specifically to defuse this.
- "Why not a bucket / boolean array of size 10^4?" — valid for the
  given constraints but it's O(max_value) space and breaks the moment
  endpoints grow to 10^9 or are floats. The sort+sweep approach is
  the one that scales.
- "Can you do it without sorting?" — only if the input is already
  sorted (then it's pure O(n) sweep) or if you're willing to use an
  interval-tree / segment-tree (O(n log n) anyway, far more code,
  same asymptotic). Sort+sweep is the right answer.
- Follow-ups they may pivot to:
    * #57 Insert Interval — input is already sorted and you insert
      one new interval; do it in O(n) without re-sorting by walking
      three phases: before, overlap-merge, after.
    * #252 Meeting Rooms — "can a person attend all meetings?" =
      "does any pair of intervals overlap after sort?"
    * #253 Meeting Rooms II — "min rooms needed" = sweep-line with
      a min-heap of end times, or the "events on a line"
      +1/-1 counter approach.
- Stability: not relevant here (we ship a new list) but if the
  interviewer asks "is this an in-place sort?", note that
  `intervals.sort(...)` mutates the input — say so, and offer
  `sorted(intervals, key=...)` if mutation is unwanted.
- Sanity-check yourself by walking [[1,3],[2,6],[8,10],[15,18]] out
  loud: hold [1,3]; see [2,6], 2 <= 3 so extend to [1,6]; see [8,10],
  8 > 6 so ship [1,6], hold [8,10]; see [15,18], ship and hold.
  Final answer: [[1,6],[8,10],[15,18]].
"""
