"""
LeetCode #238 - Product of Array Except Self  (Array - Medium)
URL: https://leetcode.com/problems/product-of-array-except-self/

Problem
-------
Given an integer array nums, return an array answer such that answer[i] is equal
to the product of all the elements of nums except nums[i].

The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit
integer.

You must write an algorithm that runs in O(n) time and WITHOUT using the division
operation.

Examples
--------
1) Input:  nums = [1,2,3,4]
   Output: [24,12,8,6]

2) Input:  nums = [-1,1,0,-3,3]
   Output: [0,0,9,0,0]

Constraints
-----------
- 2 <= nums.length <= 10^5
- -30 <= nums[i] <= 30
- The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit
  integer.

Follow-up
---------
Can you solve the problem in O(1) extra space complexity? (The output array does
not count as extra space for space complexity analysis.)

Run
---
    python 2026-06-19-product-of-array-except-self.py -v
"""

import unittest


class Solution:
    def productExceptSelf(self, nums):
        raise NotImplementedError("Implement productExceptSelf")


def brute_force(nums):
    """Reference oracle: O(n^2), allowed to use division-free multiplication."""
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

    def test_two_elements(self):
        self.assertEqual(self.sol.productExceptSelf([2, 3]), [3, 2])

    def test_two_zeros(self):
        self.assertEqual(self.sol.productExceptSelf([0, 0]), [0, 0])

    def test_single_zero(self):
        self.assertEqual(self.sol.productExceptSelf([5, 0, 2]), [0, 10, 0])

    def test_negatives(self):
        nums = [-2, -3, 4]
        self.assertEqual(self.sol.productExceptSelf(nums), brute_force(nums))

    def test_matches_brute_force_random_like(self):
        nums = [1, 5, 2, 6, 3]
        self.assertEqual(self.sol.productExceptSelf(nums), brute_force(nums))

    def test_does_not_mutate_input(self):
        nums = [1, 2, 3, 4]
        self.sol.productExceptSelf(nums)
        self.assertEqual(nums, [1, 2, 3, 4])


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  - peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
For each index, the answer is (product of everything to its LEFT) times (product
of everything to its RIGHT). Compute both with running passes - no division.

1. First pass (left to right): fill answer[i] with the product of all elements
   strictly before i. Keep a running `prefix` starting at 1; set answer[i] =
   prefix, then multiply prefix by nums[i].
2. Second pass (right to left): keep a running `suffix` starting at 1; multiply
   answer[i] by suffix, then multiply suffix by nums[i].

After both passes, answer[i] = (prefix product) * (suffix product) = product of
everything except nums[i]. Zeros are handled naturally - no special-casing and
no division by zero.

Using the output array to hold the prefix products first, then folding the
suffix in on the second pass, gives O(1) extra space (output excluded).

Complexity
----------
- Time:  O(n), two linear passes.
- Space: O(1) extra (the answer array does not count).

Python solution
---------------
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

Interview tips
--------------
- State the core identity up front: answer[i] = leftProduct[i] * rightProduct[i].
- The division trick (total product / nums[i]) is explicitly disallowed and also
  breaks on zeros - mention you avoided it deliberately.
- Reusing the output array for the prefix pass, then folding the suffix on the
  way back, achieves the O(1)-extra-space follow-up.
- Zeros need no special handling here; a single zero makes every other answer
  carry that zero, and two zeros make all answers zero - the passes do this
  automatically.
- Watch the order inside each pass: WRITE answer[i] before updating the running
  product so the current element is excluded.
"""
