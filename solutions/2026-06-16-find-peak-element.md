# LeetCode #162 - Find Peak Element

**Data structure:** Binary Search  
**Difficulty:** Medium  
**URL:** https://leetcode.com/problems/find-peak-element/

## Problem

A **peak element** is one that is strictly greater than its neighbors.

Given a 0-indexed integer array `nums`, return the index of **any** peak. You may imagine `nums[-1] = nums[n] = -∞`, so an element is always greater than an out-of-bounds neighbor.

The algorithm must run in **`O(log n)`** time.

## Examples

```text
Input: nums = [1,2,3,1]
Output: 2   (nums[2] = 3 is a peak)
```

```text
Input: nums = [1,2,1,3,5,6,4]
Output: 5   (or 1 — either peak is acceptable)
```

## Constraints

- `1 <= nums.length <= 1000`
- `-2^31 <= nums[i] <= 2^31 - 1`
- `nums[i] != nums[i + 1]` for all valid `i`.

## Approach

Binary search on the **slope**, not on sorted order.

The array is not sorted, but binary search still works: the boundary conditions (`nums[-1] = nums[n] = -∞`) guarantee a peak exists, and we can always walk uphill toward one.

At index `mid`, compare `nums[mid]` with `nums[mid + 1]`:

- If `nums[mid] < nums[mid + 1]`, the slope ascends to the right → a peak must lie to the right (values keep rising and must eventually fall at the `-∞` boundary). Set `lo = mid + 1`.
- Otherwise `nums[mid] > nums[mid + 1]`, the slope descends → a peak is at `mid` or to its left. Set `hi = mid`.

When `lo == hi`, that index is a peak.

**Complexity**

- Time: `O(log n)` — the range halves each step
- Space: `O(1)`

## Python solution

```python
class Solution:
    def findPeakElement(self, nums):
        lo, hi = 0, len(nums) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] < nums[mid + 1]:
                lo = mid + 1     # peak is to the right
            else:
                hi = mid         # peak is at mid or to the left
        return lo
```

## unittest test cases

```python
import unittest


def is_peak(nums, i):
    n = len(nums)
    left_ok = i == 0 or nums[i] > nums[i - 1]
    right_ok = i == n - 1 or nums[i] > nums[i + 1]
    return left_ok and right_ok


class TestFindPeakElement(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def assertReturnsAPeak(self, nums):
        idx = self.sol.findPeakElement(nums)
        self.assertTrue(0 <= idx < len(nums))
        self.assertTrue(is_peak(nums, idx))

    def test_example_1(self):
        self.assertEqual(self.sol.findPeakElement([1, 2, 3, 1]), 2)

    def test_example_2_any_peak(self):
        self.assertReturnsAPeak([1, 2, 1, 3, 5, 6, 4])

    def test_single_element(self):
        self.assertEqual(self.sol.findPeakElement([42]), 0)

    def test_strictly_increasing(self):
        self.assertEqual(self.sol.findPeakElement([1, 2, 3, 4, 5]), 4)

    def test_strictly_decreasing(self):
        self.assertEqual(self.sol.findPeakElement([5, 4, 3, 2, 1]), 0)
```

## Interview tips

- The key insight: binary search works without a sorted array — you search on the **direction of the slope** toward higher ground.
- Compare `mid` with `mid + 1` (not `mid - 1`) to keep index math simple; `mid + 1` is always valid while `lo < hi`.
- Adjacent elements are never equal and the virtual boundaries are `-∞`, so a peak is guaranteed — there's no "not found" case.
- Converging the range to a single index (`lo == hi`) avoids an explicit peak check inside the loop.
- A linear scan (first `i` where `nums[i] > nums[i+1]`) works but fails the `O(log n)` requirement.
