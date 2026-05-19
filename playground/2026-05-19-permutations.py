"""LeetCode #46 — Permutations  (Backtracking · Medium)

URL: https://leetcode.com/problems/permutations/

Problem
-------
Given an array `nums` of DISTINCT integers, return all the possible
permutations. You can return the answer in any order.

Examples
--------
  nums = [1,2,3]   -> [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
  nums = [0,1]     -> [[0,1],[1,0]]
  nums = [1]       -> [[1]]

Constraints
-----------
  1 <= nums.length <= 6
  -10 <= nums[i] <= 10
  All the integers of nums are unique.

Run
---
  python 2026-05-19-permutations.py -v
"""

import math
import unittest


class Solution:
    def permute(self, nums):
        raise NotImplementedError("Implement permute")


# ----------------------------- tests -----------------------------

class TestPermutations(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    @staticmethod
    def _normalize(perms):
        # Order-independent comparison: set of tuples.
        return {tuple(p) for p in perms}

    def test_example_1(self):
        out = self.sol.permute([1, 2, 3])
        expected = [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
        self.assertEqual(self._normalize(out), self._normalize(expected))
        self.assertEqual(len(out), 6)

    def test_example_2_two_elements(self):
        out = self.sol.permute([0, 1])
        self.assertEqual(self._normalize(out), {(0, 1), (1, 0)})

    def test_example_3_single(self):
        self.assertEqual(self.sol.permute([1]), [[1]])

    def test_negative_values(self):
        out = self.sol.permute([-1, 0, 1])
        self.assertEqual(len(out), 6)
        # Every permutation uses each input exactly once.
        for p in out:
            self.assertEqual(sorted(p), [-1, 0, 1])

    def test_no_duplicate_permutations(self):
        out = self.sol.permute([1, 2, 3, 4])
        self.assertEqual(len(out), 24)
        self.assertEqual(len(self._normalize(out)), 24)

    def test_count_is_factorial(self):
        for n in range(1, 7):
            nums = list(range(n))
            out = self.sol.permute(nums)
            self.assertEqual(len(out), math.factorial(n), f"n={n}")

    def test_every_permutation_is_a_valid_rearrangement(self):
        nums = [5, -2, 3, 8]
        out = self.sol.permute(nums)
        target = sorted(nums)
        for p in out:
            self.assertEqual(sorted(p), target)
            self.assertEqual(len(p), len(nums))

    def test_input_not_mutated(self):
        nums = [1, 2, 3]
        snapshot = list(nums)
        self.sol.permute(nums)
        self.assertEqual(nums, snapshot)


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  — peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
Backtracking. Build a permutation one slot at a time. At each step:
  - Try every unused number as the next pick.
  - Recurse to fill the remaining slots.
  - When the current path has length n, record a COPY of it.
  - Undo the pick before trying the next sibling (this is the "back" in
    backtracking — restoring state so the next branch starts clean).

The recursion tree has n! leaves — one per permutation.

Two common implementations
--------------------------
1. Path + used[] set: maintain a growing list `path` and a `used` set marking
   which input indices have already been placed. Most general; easiest to
   adapt to duplicates (LC 47).
2. In-place swap: swap the start index with every later index, recurse on
   start+1, swap back. O(1) extra space beyond the recursion stack and the
   output — but mutates the input during the recursion.

The path + used version is shown below; it's the form most candidates write
and the one Microsoft interviewers expect first.

Complexity
----------
- Time:  O(n * n!)   n! permutations, each costs O(n) to copy
- Space: O(n)        recursion depth + current path (excluding output)

Python solution
---------------
class Solution:
    def permute(self, nums):
        result = []
        path = []
        used = [False] * len(nums)

        def backtrack():
            if len(path) == len(nums):
                result.append(path[:])     # COPY — path keeps mutating
                return
            for i in range(len(nums)):
                if used[i]:
                    continue
                used[i] = True
                path.append(nums[i])
                backtrack()
                path.pop()                 # undo
                used[i] = False            # undo

        backtrack()
        return result

Interview tips
--------------
- State the template OUT LOUD before coding: "choose, recurse, un-choose."
  That single phrase signals you recognize it as backtracking, not brute force.
- The MOST COMMON BUG is appending `path` instead of `path[:]`. Since `path`
  is mutated throughout the recursion, you'd end up with n! references to the
  same eventually-empty list.
- Mention the complexity correctly: O(n * n!), NOT O(n!). The factor of n is
  the cost of copying the path into the result.
- For DUPLICATES (LC 47 Permutations II), sort first and add the standard
  skip: `if i > 0 and nums[i] == nums[i-1] and not used[i-1]: continue`.
  Mention this even if not asked — it shows you've seen the variant.
- Microsoft loves the follow-up: "What if n is large (say 12) and you only
  need ONE random permutation?" Answer: Fisher–Yates shuffle in O(n).
- itertools.permutations(nums) is the Pythonic one-liner. Acknowledge it but
  implement the backtracking version — interviewers want to see the recursion.
"""
