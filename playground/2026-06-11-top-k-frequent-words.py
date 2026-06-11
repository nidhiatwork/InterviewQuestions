"""
LeetCode #692 - Top K Frequent Words  (Heap (Priority Queue) - Medium)
URL: https://leetcode.com/problems/top-k-frequent-words/

Problem
-------
Given an array of strings words and an integer k, return the k most frequent
strings.

Return the answer sorted by the frequency from highest to lowest. Sort the words
with the same frequency by their lexicographical order.

Examples
--------
1) Input:  words = ["i","love","leetcode","i","love","coding"], k = 2
   Output: ["i","love"]
   Explanation: "i" and "love" are the two most frequent words. Note that "i"
   comes before "love" due to a lower alphabetical order.

2) Input:  words = ["the","day","is","sunny","the","the","the","sunny","is","is"], k = 4
   Output: ["the","is","sunny","day"]
   Explanation: "the", "is", "sunny" and "day" are the four most frequent words,
   with the number of occurrences being 4, 3, 2 and 1 respectively.

Constraints
-----------
- 1 <= words.length <= 500
- 1 <= words[i].length <= 10
- words[i] consists of lowercase English letters.
- k is in the range [1, The number of unique words[i]]

Follow-up
---------
Could you solve it in O(n log k) time and O(n) extra space?

Run
---
    python 2026-06-11-top-k-frequent-words.py -v
"""

import unittest


class Solution:
    def topKFrequent(self, words, k):
        raise NotImplementedError("Implement topKFrequent")


class TestTopKFrequentWords(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1(self):
        words = ["i", "love", "leetcode", "i", "love", "coding"]
        self.assertEqual(self.sol.topKFrequent(words, 2), ["i", "love"])

    def test_example_2(self):
        words = ["the", "day", "is", "sunny", "the", "the", "the", "sunny", "is", "is"]
        self.assertEqual(
            self.sol.topKFrequent(words, 4), ["the", "is", "sunny", "day"]
        )

    def test_tie_broken_lexicographically(self):
        words = ["b", "a", "c", "a", "b", "c"]
        # all frequency 2 -> alphabetical order
        self.assertEqual(self.sol.topKFrequent(words, 2), ["a", "b"])

    def test_single_word(self):
        self.assertEqual(self.sol.topKFrequent(["hello"], 1), ["hello"])

    def test_k_equals_unique_count(self):
        words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
        self.assertEqual(
            self.sol.topKFrequent(words, 3), ["apple", "banana", "cherry"]
        )

    def test_all_distinct_words_alphabetical(self):
        words = ["zebra", "monkey", "apple", "lion"]
        self.assertEqual(self.sol.topKFrequent(words, 2), ["apple", "lion"])

    def test_frequency_dominates_over_alpha(self):
        words = ["aaa", "bbb", "bbb", "ccc", "ccc", "ccc"]
        self.assertEqual(self.sol.topKFrequent(words, 1), ["ccc"])


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  - peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
Count, then use a heap of size k with a carefully chosen ordering.

1. Count each word's frequency with a hash map (Counter).
2. We want the k words with the highest frequency, breaking ties by smallest
   lexicographic order. We keep a MIN-heap of at most k elements so the "worst"
   candidate sits on top and gets evicted first.

The tricky part is the comparison. The element that should be evicted first
(the heap top) is the one with the LOWEST frequency, and among equal
frequencies, the one with the LARGEST word (because larger words should drop
out, smaller words win ties). To get that with Python's min-heap we push the key
(freq, NEG-word-order). Since strings cannot be negated directly, we wrap the
word so that larger words compare as "smaller" on the heap.

A clean way: push (count, word) into a min-heap but invert the word comparison
by using a wrapper, OR push (-count, word) into a min-heap of all items and pop
k times (simplest to reason about):

  - heap key = (-count, word). The natural min-heap order then gives highest
    count first, and for equal counts, smallest word first. Pop k times.
  - That is O(n log n). For the O(n log k) follow-up, keep a size-k heap with the
    inverted comparison via a wrapper class.

Below is the simple, interview-safe O(n + m log m) version (m = unique words),
followed by the O(n log k) heap-of-size-k variant in the notes.

Complexity
----------
- Simple version: O(n + m log m) time, O(m) space (m = unique words).
- Size-k heap version: O(n log k) time, O(n) space (the follow-up target).

Python solution
---------------
import heapq
from collections import Counter


class Solution:
    def topKFrequent(self, words, k):
        counts = Counter(words)
        # Min-heap of size k. Comparison wrapper makes the "worst" item pop first:
        # lowest frequency first, and for equal frequency, lexicographically
        # LARGER word first (so it gets evicted, keeping smaller words).
        heap = []
        for word, freq in counts.items():
            heapq.heappush(heap, _Item(word, freq))
            if len(heap) > k:
                heapq.heappop(heap)
        # Heap now holds the k best, worst on top. Pop all and reverse.
        result = []
        while heap:
            result.append(heapq.heappop(heap).word)
        result.reverse()
        return result


class _Item:
    def __init__(self, word, freq):
        self.word = word
        self.freq = freq

    def __lt__(self, other):
        if self.freq != other.freq:
            return self.freq < other.freq      # lower freq is "less" -> pops first
        return self.word > other.word          # larger word is "less" -> pops first


Simple alternative (O(n + m log m)), easiest to state out loud:

    import heapq
    from collections import Counter

    class Solution:
        def topKFrequent(self, words, k):
            counts = Counter(words)
            return heapq.nsmallest(
                k, counts.keys(), key=lambda w: (-counts[w], w)
            )

Interview tips
--------------
- The sort key (-count, word) captures both rules at once: highest frequency
  first, ties broken by smallest word.
- heapq.nsmallest with that key is the cleanest one-liner and runs in O(m log k).
- If asked to avoid the key trick, build a max-heap of (-count, word) and pop k
  times; remember Python heaps are min-heaps so you negate the count.
- The size-k min-heap with a custom __lt__ achieves the O(n log k) follow-up but
  is fiddly because the tie-break direction must be inverted on the heap.
- Watch the tie-break direction carefully: for the heap-of-size-k, the word that
  should be DROPPED (larger lexicographically) must compare as smaller.
"""
