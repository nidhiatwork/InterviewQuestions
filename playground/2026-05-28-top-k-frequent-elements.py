"""LeetCode #347 — Top K Frequent Elements  (Heap (Priority Queue) · Medium)

URL: https://leetcode.com/problems/top-k-frequent-elements/

Problem
-------
Given an integer array nums and an integer k, return the k most frequent
elements. You may return the answer in any order.

Examples
--------
  nums = [1,1,1,2,2,3], k = 2   ->  [1, 2]
  nums = [1], k = 1             ->  [1]
  nums = [4,1,-1,2,-1,2,3], k = 2 -> [-1, 2]   (any order)

Constraints
-----------
  1 <= nums.length <= 10^5
  -10^4 <= nums[i] <= 10^4
  k is in the range [1, the number of unique elements in the array].
  It is guaranteed that the answer is unique.

Follow-up
---------
  Your algorithm's time complexity must be better than O(n log n), where n is
  the array's size.

Run
---
  python 2026-05-28-top-k-frequent-elements.py -v
"""

import unittest


class Solution:
    def topKFrequent(self, nums, k):
        raise NotImplementedError("Implement topKFrequent")


# ----------------------------- tests -----------------------------

class TestTopKFrequent(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1(self):
        result = self.sol.topKFrequent([1, 1, 1, 2, 2, 3], 2)
        self.assertEqual(sorted(result), [1, 2])

    def test_example_2_single_element(self):
        self.assertEqual(self.sol.topKFrequent([1], 1), [1])

    def test_mixed_negatives(self):
        result = self.sol.topKFrequent([4, 1, -1, 2, -1, 2, 3], 2)
        self.assertEqual(sorted(result), [-1, 2])

    def test_k_equals_unique_count(self):
        result = self.sol.topKFrequent([1, 2, 3, 4], 4)
        self.assertEqual(sorted(result), [1, 2, 3, 4])

    def test_all_same_frequency(self):
        # Every element appears once; any k of them is valid.
        result = self.sol.topKFrequent([5, 6, 7, 8], 2)
        self.assertEqual(len(result), 2)
        self.assertTrue(set(result).issubset({5, 6, 7, 8}))

    def test_one_dominant_element(self):
        nums = [9] * 100 + [1, 2, 3]
        result = self.sol.topKFrequent(nums, 1)
        self.assertEqual(result, [9])

    def test_three_tiers(self):
        # 7 appears 4x, 8 appears 3x, 9 appears 2x, 10 appears 1x
        nums = [7, 7, 7, 7, 8, 8, 8, 9, 9, 10]
        result = self.sol.topKFrequent(nums, 3)
        self.assertEqual(sorted(result), [7, 8, 9])

    def test_large_k_after_dedup(self):
        nums = list(range(1, 11)) * 2  # each of 1..10 appears twice
        result = self.sol.topKFrequent(nums, 5)
        self.assertEqual(len(result), 5)
        self.assertTrue(set(result).issubset(set(range(1, 11))))


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  — peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
Three solid framings, in increasing order of cleverness:

1. Heap (the canonical "heap problem" answer)
   - Count frequencies with a Counter -> dict {value: count}.
   - Push each (count, value) pair onto a min-heap of size k.
   - When the heap exceeds k, pop the smallest. After processing all unique
     values, the heap holds the k most frequent.
   - Time:  O(n + u log k)  where u = number of unique values
   - Space: O(u)

2. nlargest (idiomatic Python, same big-O as heap)
   - Counter then heapq.nlargest(k, counter.keys(), key=counter.get)
   - One line. In interviews, mention this exists, then show the manual
     heap to prove you know what's underneath.

3. Bucket sort (beats the n log n follow-up)
   - Frequency is bounded by n, so build buckets[freq] = list of values with
     that frequency. Walk buckets from index n down to 1 and collect the
     first k values.
   - Time:  O(n)
   - Space: O(n)
   - This is the answer to the follow-up "faster than n log n."

Default to the heap framing because the rotation slot is Heap — but lead the
discussion with bucket sort if the interviewer pushes on the follow-up.

Complexity
----------
- Time:  O(n + u log k)  heap  /  O(n) bucket sort
- Space: O(u + k)        heap  /  O(n) bucket sort  (u = unique value count)

Python solution
---------------
import heapq
from collections import Counter

class Solution:
    def topKFrequent(self, nums, k):
        counts = Counter(nums)
        heap = []  # min-heap of (count, value), size <= k
        for value, count in counts.items():
            heapq.heappush(heap, (count, value))
            if len(heap) > k:
                heapq.heappop(heap)
        return [value for _, value in heap]

# Bucket-sort variant for the O(n) follow-up:
#
# from collections import Counter
#
# class Solution:
#     def topKFrequent(self, nums, k):
#         counts = Counter(nums)
#         buckets = [[] for _ in range(len(nums) + 1)]
#         for value, count in counts.items():
#             buckets[count].append(value)
#         out = []
#         for freq in range(len(buckets) - 1, 0, -1):
#             for value in buckets[freq]:
#                 out.append(value)
#                 if len(out) == k:
#                     return out
#         return out

Interview tips
--------------
- Open by separating the two phases: (a) tally frequencies, (b) pick top-k.
  Phase (a) is unavoidable O(n) — the interesting design choice is phase (b).
- Default to the size-k min-heap, NOT a max-heap of size u. The trick is to
  keep only k candidates alive; that's what gets you u log k instead of
  u log u.
- For the "faster than n log n" follow-up, jump straight to bucket sort
  using freq -> values. The bound that makes it work: a frequency can never
  exceed len(nums), so the bucket array has size n + 1.
- Microsoft loves to ask for the streaming variant: "what if nums is a
  stream and k can change?" -> maintain Counter + a balanced BST keyed by
  (count, value), or a heap with lazy deletion. Mention it; don't implement
  unless asked.
- Tie-breaking: the problem guarantees a unique answer, so you don't have
  to define an order. If they remove that guarantee, ask which tiebreaker
  they want (lex order? insertion order?) before coding.
"""
