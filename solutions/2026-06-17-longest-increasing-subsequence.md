# LeetCode #300 - Longest Increasing Subsequence

**Data structure:** Binary Search  
**Difficulty:** Medium  
**URL:** https://leetcode.com/problems/longest-increasing-subsequence/

## Problem

Given an integer array `nums`, return the length of the longest **strictly increasing** subsequence.

A subsequence is derived by deleting some or no elements without changing the order of the remaining elements.

## Examples

```text
Input: nums = [10,9,2,5,3,7,101,18]
Output: 4   (e.g. [2,3,7,101])
```

```text
Input: nums = [0,1,0,3,2,3]
Output: 4   (e.g. [0,1,2,3])
```

```text
Input: nums = [7,7,7,7,7,7,7]
Output: 1
```

## Constraints

- `1 <= nums.length <= 2500`
- `-10^4 <= nums[i] <= 10^4`

**Follow-up:** Achieve `O(n log n)` time.

## Approach

Maintain a running **tails** array using a greedy rule plus binary search (the patience-sorting idea).

Walk through `nums` once. Keep a list `tails`, where `tails[i]` is the **smallest possible tail value** of any increasing subsequence of length `i + 1` seen so far. This list stays sorted, which is what lets us binary search it.

For each number `x`:

- Binary search `tails` for the leftmost position whose value is `>= x`.
- If found, overwrite it with `x` — keeping that length's tail as small as possible leaves more room to extend later.
- If `x` exceeds every tail, append it — we extended the best run by one, so the answer grows.

The final length of `tails` is the LIS length. Note `tails` is **not** an actual subsequence — only its length matters.

Keeping each length's tail minimal is always at least as good as a larger tail (a smaller tail can be extended by more future values), and the sorted invariant makes each insertion an `O(log n)` search.

**Complexity**

- Time: `O(n log n)` — one binary search per element
- Space: `O(n)` for the tails list

## Python solution

```python
import bisect


class Solution:
    def lengthOfLIS(self, nums):
        tails = []
        for x in nums:
            pos = bisect.bisect_left(tails, x)   # leftmost tail >= x
            if pos == len(tails):
                tails.append(x)                  # x extends the longest run
            else:
                tails[pos] = x                   # keep this length's tail minimal
        return len(tails)
```

## unittest test cases

```python
import unittest


class TestLengthOfLIS(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1(self):
        self.assertEqual(self.sol.lengthOfLIS([10, 9, 2, 5, 3, 7, 101, 18]), 4)

    def test_example_2(self):
        self.assertEqual(self.sol.lengthOfLIS([0, 1, 0, 3, 2, 3]), 4)

    def test_all_equal(self):
        self.assertEqual(self.sol.lengthOfLIS([7, 7, 7, 7, 7, 7, 7]), 1)

    def test_strictly_increasing(self):
        self.assertEqual(self.sol.lengthOfLIS([1, 2, 3, 4, 5]), 5)

    def test_strictly_decreasing(self):
        self.assertEqual(self.sol.lengthOfLIS([5, 4, 3, 2, 1]), 1)

    def test_duplicates_break_run(self):
        self.assertEqual(self.sol.lengthOfLIS([1, 3, 3, 3, 4]), 3)
```

## Interview tips

- Frame it as a streaming/greedy method: scan once, keep the smallest tail for each achievable length, and binary search to place each value.
- `bisect_left` gives **strictly** increasing (it replaces an equal value, so duplicates don't extend the run). For non-strict, use `bisect_right`.
- `tails` is not the subsequence itself — only its length is the answer. Reconstructing the actual subsequence needs extra index bookkeeping.
- The simpler `O(n^2)` approach (for each `i`, scan all `j < i`) is a fine baseline, but the tails + binary search method hits the `O(n log n)` follow-up.
- Watch the strict-vs-non-strict distinction — it's the most common bug here.
