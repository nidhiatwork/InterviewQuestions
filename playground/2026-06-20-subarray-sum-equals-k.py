"""
LeetCode #560 - Subarray Sum Equals K  (Hash Table - Medium)
URL: https://leetcode.com/problems/subarray-sum-equals-k/

Problem
-------
Given an array of integers nums and an integer k, return the total number of
subarrays whose sum equals to k.

A subarray is a contiguous non-empty sequence of elements within an array.

Examples
--------
1) Input:  nums = [1,1,1], k = 2
   Output: 2
   Explanation: The subarrays [1,1] (indices 0-1) and [1,1] (indices 1-2) both
   sum to 2.

2) Input:  nums = [1,2,3], k = 3
   Output: 2
   Explanation: [1,2] and [3] both sum to 3.

Constraints
-----------
- 1 <= nums.length <= 2 * 10^4
- -1000 <= nums[i] <= 1000
- -10^7 <= k <= 10^7

Run
---
    python 2026-06-20-subarray-sum-equals-k.py -v
"""

import unittest


class Solution:
    def subarraySum(self, nums, k):
        raise NotImplementedError("Implement subarraySum")


def brute_force(nums, k):
    """Reference oracle: O(n^2) count of subarrays summing to k."""
    count = 0
    n = len(nums)
    for i in range(n):
        total = 0
        for j in range(i, n):
            total += nums[j]
            if total == k:
                count += 1
    return count


class TestSubarraySum(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1(self):
        self.assertEqual(self.sol.subarraySum([1, 1, 1], 2), 2)

    def test_example_2(self):
        self.assertEqual(self.sol.subarraySum([1, 2, 3], 3), 2)

    def test_single_element_match(self):
        self.assertEqual(self.sol.subarraySum([5], 5), 1)

    def test_single_element_no_match(self):
        self.assertEqual(self.sol.subarraySum([5], 3), 0)

    def test_with_negatives(self):
        nums = [1, -1, 1, -1]
        self.assertEqual(self.sol.subarraySum(nums, 0), brute_force(nums, 0))

    def test_zeros_and_k_zero(self):
        nums = [0, 0, 0]
        self.assertEqual(self.sol.subarraySum(nums, 0), brute_force(nums, 0))

    def test_k_negative(self):
        nums = [-1, -1, 1]
        self.assertEqual(self.sol.subarraySum(nums, -2), brute_force(nums, -2))

    def test_no_subarray(self):
        self.assertEqual(self.sol.subarraySum([1, 2, 3], 100), 0)

    def test_matches_brute_force_mixed(self):
        nums = [3, 4, 7, 2, -3, 1, 4, 2]
        self.assertEqual(self.sol.subarraySum(nums, 7), brute_force(nums, 7))


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  - peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
Use running prefix sums plus a hash map of how many times each prefix sum has
occurred.

The sum of the subarray ending at index j and starting just after index i is
prefix[j] - prefix[i]. We want this to equal k, i.e. prefix[i] = prefix[j] - k.
So as we sweep j from left to right and maintain the current running prefix sum,
the number of valid subarrays ending at j is exactly how many earlier prefix
sums equal (current_prefix - k).

Algorithm:
  - Keep a dict `seen` mapping prefix-sum value -> count of indices with that
    prefix sum. Initialize seen[0] = 1 to account for subarrays that start at
    index 0 (a prefix sum of exactly k with no earlier prefix subtracted).
  - Maintain running `prefix`. For each num: add it to prefix, then add
    seen.get(prefix - k, 0) to the answer, then increment seen[prefix].

This handles negatives and zeros correctly because we are counting prefix-sum
occurrences, not using a sliding window (a window would fail with negatives).

Complexity
----------
- Time:  O(n), single pass with O(1) dict operations.
- Space: O(n) for the prefix-sum counts.

Python solution
---------------
from collections import defaultdict


class Solution:
    def subarraySum(self, nums, k):
        seen = defaultdict(int)
        seen[0] = 1                 # empty prefix enables subarrays from index 0
        prefix = 0
        count = 0
        for num in nums:
            prefix += num
            count += seen[prefix - k]
            seen[prefix] += 1
        return count

Interview tips
--------------
- The key identity: a subarray sums to k iff (current prefix - k) was a previous
  prefix sum. Count those occurrences.
- Initialize seen[0] = 1 - forgetting this misses subarrays that start at index
  0 and is the classic bug.
- A sliding window does NOT work here because negative numbers break the
  monotonic-growth assumption; the prefix-sum + hashmap method is required.
- Add to the answer BEFORE inserting the current prefix, so you never count the
  zero-length subarray for the current index.
- Mention it generalizes: the same prefix-sum-count trick counts subarrays with a
  given XOR, or finds the longest subarray summing to k (store first index
  instead of counts).
"""
