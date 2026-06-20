# LeetCode #560 - Subarray Sum Equals K

**Data structure:** Hash Table  
**Difficulty:** Medium  
**URL:** https://leetcode.com/problems/subarray-sum-equals-k/

## Problem

Given an array of integers `nums` and an integer `k`, return the total number of contiguous, non-empty subarrays whose sum equals `k`.

## Examples

```text
Input: nums = [1,1,1], k = 2
Output: 2   ([1,1] at 0-1 and [1,1] at 1-2)
```

```text
Input: nums = [1,2,3], k = 3
Output: 2   ([1,2] and [3])
```

## Constraints

- `1 <= nums.length <= 2 * 10^4`
- `-1000 <= nums[i] <= 1000`
- `-10^7 <= k <= 10^7`

## Approach

Use running **prefix sums** plus a hash map of how many times each prefix sum has occurred.

The sum of the subarray ending at index `j` and starting just after index `i` is `prefix[j] - prefix[i]`. We want it to equal `k`, i.e. `prefix[i] = prefix[j] - k`. So as we sweep `j` left to right maintaining the running prefix sum, the number of valid subarrays ending at `j` is exactly how many earlier prefix sums equal `current_prefix - k`.

Algorithm:

- Keep a dict `seen` mapping prefix-sum value → count. Initialize `seen[0] = 1` to account for subarrays starting at index 0.
- Maintain running `prefix`. For each `num`: add it to `prefix`, add `seen.get(prefix - k, 0)` to the answer, then increment `seen[prefix]`.

This handles negatives and zeros correctly because we count prefix-sum occurrences rather than using a sliding window (a window fails with negatives).

**Complexity**

- Time: `O(n)` — single pass
- Space: `O(n)` for the prefix-sum counts

## Python solution

```python
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
```

## unittest test cases

```python
import unittest


def brute_force(nums, k):
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

    def test_with_negatives(self):
        nums = [1, -1, 1, -1]
        self.assertEqual(self.sol.subarraySum(nums, 0), brute_force(nums, 0))

    def test_zeros_and_k_zero(self):
        nums = [0, 0, 0]
        self.assertEqual(self.sol.subarraySum(nums, 0), brute_force(nums, 0))

    def test_no_subarray(self):
        self.assertEqual(self.sol.subarraySum([1, 2, 3], 100), 0)
```

## Interview tips

- The key identity: a subarray sums to `k` iff `current_prefix - k` was a previous prefix sum — count those occurrences.
- Initialize `seen[0] = 1` — forgetting this misses subarrays that start at index 0 and is the classic bug.
- A sliding window does **not** work here because negatives break the monotonic-growth assumption; prefix-sum + hashmap is required.
- Add to the answer **before** inserting the current prefix, so you never count the zero-length subarray for the current index.
- It generalizes: the same trick counts subarrays with a given XOR, or finds the longest subarray summing to `k` (store first index instead of counts).
