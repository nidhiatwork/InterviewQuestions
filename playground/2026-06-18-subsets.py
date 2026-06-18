"""
LeetCode #78 - Subsets  (Backtracking - Medium)
URL: https://leetcode.com/problems/subsets/

Problem
-------
Given an integer array nums of unique elements, return all possible subsets (the
power set).

The solution set must not contain duplicate subsets. Return the solution in any
order.

Examples
--------
1) Input:  nums = [1,2,3]
   Output: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]

2) Input:  nums = [0]
   Output: [[],[0]]

Constraints
-----------
- 1 <= nums.length <= 10
- -10 <= nums[i] <= 10
- All the numbers of nums are unique.

Run
---
    python 2026-06-18-subsets.py -v
"""

import unittest


class Solution:
    def subsets(self, nums):
        raise NotImplementedError("Implement subsets")


def normalize(subsets):
    """Sort each subset and the overall list so comparison is order-independent."""
    return sorted([sorted(s) for s in subsets])


class TestSubsets(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1(self):
        result = self.sol.subsets([1, 2, 3])
        expected = [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]
        self.assertEqual(normalize(result), normalize(expected))

    def test_single_element(self):
        result = self.sol.subsets([0])
        self.assertEqual(normalize(result), normalize([[], [0]]))

    def test_count_is_power_of_two(self):
        nums = [1, 2, 3, 4]
        result = self.sol.subsets(nums)
        self.assertEqual(len(result), 2 ** len(nums))

    def test_no_duplicate_subsets(self):
        nums = [5, 6, 7]
        result = self.sol.subsets(nums)
        as_tuples = [tuple(sorted(s)) for s in result]
        self.assertEqual(len(as_tuples), len(set(as_tuples)))

    def test_contains_empty_and_full(self):
        nums = [1, 2]
        result = normalize(self.sol.subsets(nums))
        self.assertIn([], result)
        self.assertIn([1, 2], result)

    def test_negative_numbers(self):
        result = self.sol.subsets([-1, 2])
        expected = [[], [-1], [2], [-1, 2]]
        self.assertEqual(normalize(result), normalize(expected))

    def test_two_elements_all_subsets(self):
        result = self.sol.subsets([9, 8])
        expected = [[], [9], [8], [9, 8]]
        self.assertEqual(normalize(result), normalize(expected))


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  - peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
Backtracking: at each index decide to include or skip that element, recording a
subset at every node of the decision tree.

Use a recursive helper that takes a start index and the current partial subset:
  - Record a COPY of the current subset (every recursion node is a valid subset,
    including the empty one at the very start).
  - For each index i from start to the end:
      * Choose nums[i] (append it).
      * Recurse with start = i + 1 so we never reuse earlier elements and never
        produce permutations of the same set.
      * Un-choose (pop) to backtrack and try the next candidate.

Because we always advance the start index, each subset is generated exactly once
in a fixed (increasing-index) order, so there are no duplicates.

There are 2^n subsets, and we copy each one, so the work is bounded by the output
size.

Complexity
----------
- Time:  O(n * 2^n), 2^n subsets, each up to length n to copy.
- Space: O(n) recursion depth (excluding the output list).

Python solution
---------------
class Solution:
    def subsets(self, nums):
        result = []

        def backtrack(start, path):
            result.append(path[:])           # record current subset
            for i in range(start, len(nums)):
                path.append(nums[i])         # choose
                backtrack(i + 1, path)       # explore (i+1 avoids reuse/dups)
                path.pop()                   # un-choose

        backtrack(0, [])
        return result

Interview tips
--------------
- Record a subset at EVERY node, not only at the leaves - the empty set and all
  partial sets are valid subsets.
- Passing start = i + 1 (not 0) is what prevents duplicates and permutations.
- Append a COPY (path[:]) - appending the live list would later be mutated by
  backtracking.
- Two clean alternatives: (a) iterative - start with [[]] and, for each num,
  add it to every existing subset; (b) bitmask - iterate masks 0..2^n - 1 and
  include nums[j] when bit j is set.
- The bitmask version is a great one-liner to mention for n <= 20-ish.
"""
