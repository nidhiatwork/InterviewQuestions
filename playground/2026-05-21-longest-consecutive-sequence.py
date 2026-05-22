"""
LeetCode #128 — Longest Consecutive Sequence  (Hash Table · Medium)
URL: https://leetcode.com/problems/longest-consecutive-sequence/

Problem
-------
Given an unsorted array of integers `nums`, return the length of the longest
consecutive elements sequence.

You must write an algorithm that runs in O(n) time.

Examples
--------
1) Input:  nums = [100, 4, 200, 1, 3, 2]
   Output: 4
   Explanation: The longest consecutive elements sequence is [1, 2, 3, 4]. Length = 4.

2) Input:  nums = [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]
   Output: 9
   Explanation: [0, 1, 2, 3, 4, 5, 6, 7, 8] is the longest consecutive sequence. Length = 9.

3) Input:  nums = [1, 0, 1, 2]
   Output: 3
   Explanation: Duplicates don't extend a sequence — [0, 1, 2] gives 3.

Constraints
-----------
- 0 <= nums.length <= 10^5
- -10^9 <= nums[i] <= 10^9

Run
---
    python 2026-05-21-longest-consecutive-sequence.py -v
"""

import unittest


class Solution:
    def longestConsecutive(self, nums):
        raise NotImplementedError("Implement longestConsecutive")


class TestLongestConsecutive(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1(self):
        self.assertEqual(self.sol.longestConsecutive([100, 4, 200, 1, 3, 2]), 4)

    def test_example_2(self):
        self.assertEqual(
            self.sol.longestConsecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]), 9
        )

    def test_duplicates_do_not_extend(self):
        self.assertEqual(self.sol.longestConsecutive([1, 0, 1, 2]), 3)

    def test_empty_array(self):
        self.assertEqual(self.sol.longestConsecutive([]), 0)

    def test_single_element(self):
        self.assertEqual(self.sol.longestConsecutive([7]), 1)

    def test_all_same(self):
        self.assertEqual(self.sol.longestConsecutive([5, 5, 5, 5]), 1)

    def test_negatives_and_positives(self):
        self.assertEqual(self.sol.longestConsecutive([-3, -2, -1, 0, 1, 5, 6]), 5)

    def test_no_consecutive(self):
        self.assertEqual(self.sol.longestConsecutive([10, 30, 50, 70]), 1)

    def test_two_separate_runs(self):
        # [1,2,3] and [10,11,12,13] -> longer one wins.
        self.assertEqual(self.sol.longestConsecutive([3, 1, 11, 2, 12, 10, 13]), 4)

    def test_large_range(self):
        nums = list(range(1000, 0, -1))  # 1000..1
        self.assertEqual(self.sol.longestConsecutive(nums), 1000)


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  — peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
The naive idea is to sort and then walk the array counting consecutive runs —
that's O(n log n). The interview-favourite O(n) solution uses a hash set:

1. Insert every number into a set `s` (this also drops duplicates).
2. For each number `n` in `s`, only start counting a run if `n - 1` is NOT in
   the set. That guarantees `n` is the smallest element of its run, so we
   visit each run exactly once.
3. From that starting point, keep incrementing `cur = n + 1` while `cur` is in
   the set, tracking the run length. Update `best` with the run length.
4. Return `best` (0 for empty input).

Why is it O(n) overall? Each element is visited at most twice — once when we
iterate the set, and at most once as part of a run extension. The "start of
run" gate (`n - 1 not in s`) is what makes that bound hold.

Complexity
----------
- Time:  O(n)        — set ops are O(1) amortized; each element joins ≤ 1 run.
- Space: O(n)        — the hash set.

Python solution
---------------
class Solution:
    def longestConsecutive(self, nums):
        if not nums:
            return 0
        s = set(nums)
        best = 0
        for n in s:
            if (n - 1) not in s:
                cur = n
                run = 1
                while (cur + 1) in s:
                    cur += 1
                    run += 1
                if run > best:
                    best = run
        return best

Interview tips
--------------
- State the O(n log n) sort baseline first, then upgrade to the hash-set
  approach. Interviewers want to hear the trade-off.
- The keystone insight is the "only start from a run head" trick. If you skip
  it and start a while-loop from every element, the algorithm degrades to
  O(n^2) on worst-case input like [1,2,3,...,n].
- Watch for the empty-array edge case — return 0, don't crash on max().
- Duplicates should NOT extend a run — converting to a set handles this for
  free, but call it out explicitly.
- If asked to also RETURN the run itself (not just the length), track the run
  start as well as the length and reconstruct it at the end.
- Variants worth knowing: "Longest consecutive sequence in a binary tree"
  (LC 298), and the union-find formulation (overkill here but useful framing).
"""
