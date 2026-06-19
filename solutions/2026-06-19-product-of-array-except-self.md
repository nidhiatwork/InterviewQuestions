# LeetCode #238 - Product of Array Except Self

**Data structure:** Array  
**Difficulty:** Medium  
**URL:** https://leetcode.com/problems/product-of-array-except-self/

## Problem

Given an integer array `nums`, return an array `answer` such that `answer[i]` equals the product of all elements of `nums` **except** `nums[i]`.

You must run in `O(n)` time and **without division**.

## Examples

```text
Input: nums = [1,2,3,4]
Output: [24,12,8,6]
```

```text
Input: nums = [-1,1,0,-3,3]
Output: [0,0,9,0,0]
```

## Constraints

- `2 <= nums.length <= 10^5`
- `-30 <= nums[i] <= 30`
- The product of any prefix or suffix fits in a 32-bit integer.

**Follow-up:** Solve in `O(1)` extra space (the output array doesn't count).

## Approach

For each index, the answer is **(product of everything to its left) × (product of everything to its right)**. Compute both with running passes — no division.

1. **Left-to-right pass:** fill `answer[i]` with the product of all elements strictly before `i`. Keep a running `prefix` starting at 1; set `answer[i] = prefix`, then multiply `prefix` by `nums[i]`.
2. **Right-to-left pass:** keep a running `suffix` starting at 1; multiply `answer[i]` by `suffix`, then multiply `suffix` by `nums[i]`.

After both passes, `answer[i]` is the product of everything except `nums[i]`. Zeros are handled naturally — no special-casing and no division by zero.

Using the output array for the prefix products, then folding the suffix in on the second pass, gives `O(1)` extra space.

**Complexity**

- Time: `O(n)` — two linear passes
- Space: `O(1)` extra (output array excluded)

## Python solution

```python
class Solution:
    def productExceptSelf(self, nums):
        n = len(nums)
        answer = [1] * n

        prefix = 1
        for i in range(n):
            answer[i] = prefix          # product of everything before i
            prefix *= nums[i]

        suffix = 1
        for i in range(n - 1, -1, -1):
            answer[i] *= suffix         # fold in product of everything after i
            suffix *= nums[i]

        return answer
```

## unittest test cases

```python
import unittest


def brute_force(nums):
    n = len(nums)
    result = []
    for i in range(n):
        product = 1
        for j in range(n):
            if j != i:
                product *= nums[j]
        result.append(product)
    return result


class TestProductExceptSelf(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1(self):
        self.assertEqual(self.sol.productExceptSelf([1, 2, 3, 4]), [24, 12, 8, 6])

    def test_example_2_with_zero(self):
        self.assertEqual(
            self.sol.productExceptSelf([-1, 1, 0, -3, 3]), [0, 0, 9, 0, 0]
        )

    def test_single_zero(self):
        self.assertEqual(self.sol.productExceptSelf([5, 0, 2]), [0, 10, 0])

    def test_two_zeros(self):
        self.assertEqual(self.sol.productExceptSelf([0, 0]), [0, 0])

    def test_matches_brute_force(self):
        nums = [1, 5, 2, 6, 3]
        self.assertEqual(self.sol.productExceptSelf(nums), brute_force(nums))
```

## Interview tips

- State the identity up front: `answer[i] = leftProduct[i] * rightProduct[i]`.
- The division trick (total product / `nums[i]`) is explicitly disallowed and also breaks on zeros — mention you avoided it deliberately.
- Reusing the output array for the prefix pass, then folding the suffix on the way back, achieves the `O(1)`-extra-space follow-up.
- Zeros need no special handling: one zero makes every other answer carry it, two zeros make all answers zero — the passes do this automatically.
- Watch the order inside each pass: **write** `answer[i]` before updating the running product so the current element is excluded.
