# LeetCode #692 - Top K Frequent Words

**Data structure:** Heap (Priority Queue)  
**Difficulty:** Medium  
**URL:** https://leetcode.com/problems/top-k-frequent-words/

## Problem

Given an array of strings `words` and an integer `k`, return the `k` most frequent strings.

Return the answer sorted by frequency from highest to lowest. Words with the same frequency are sorted by their **lexicographical order**.

## Examples

```text
Input: words = ["i","love","leetcode","i","love","coding"], k = 2
Output: ["i","love"]
("i" and "love" both appear twice; "i" comes first alphabetically)
```

```text
Input: words = ["the","day","is","sunny","the","the","the","sunny","is","is"], k = 4
Output: ["the","is","sunny","day"]
(frequencies 4, 3, 2, 1 respectively)
```

## Constraints

- `1 <= words.length <= 500`
- `1 <= words[i].length <= 10`
- `words[i]` consists of lowercase English letters.
- `k` is in the range `[1, number of unique words]`

**Follow-up:** Solve it in `O(n log k)` time and `O(n)` extra space.

## Approach

Count frequencies, then select the top `k` using a heap with a tie-aware ordering.

1. Count each word's frequency with a hash map (`Counter`).
2. We want the `k` words with the highest frequency, breaking ties by the **smallest** lexicographic word.

The sort key `(-count, word)` captures both rules in one comparison: most frequent first, and among equal frequencies, the alphabetically smaller word first. Using `heapq.nsmallest(k, keys, key=lambda w: (-counts[w], w))` gives the answer directly in `O(m log k)` where `m` is the number of unique words.

For the strict `O(n log k)` follow-up, maintain a min-heap of size `k`. The item that should be evicted first (heap top) is the one with the **lowest** frequency, and among equal frequencies, the **lexicographically larger** word — so the tie-break direction must be inverted on the heap via a custom comparator.

**Complexity**

- Simple version: `O(n + m log m)` time, `O(m)` space
- Size-`k` heap version: `O(n log k)` time, `O(n)` space (the follow-up target)

## Python solution

```python
import heapq
from collections import Counter


class Solution:
    def topKFrequent(self, words, k):
        counts = Counter(words)
        return heapq.nsmallest(
            k, counts.keys(), key=lambda w: (-counts[w], w)
        )
```

Size-`k` heap variant (`O(n log k)` follow-up):

```python
import heapq
from collections import Counter


class _Item:
    def __init__(self, word, freq):
        self.word = word
        self.freq = freq

    def __lt__(self, other):
        if self.freq != other.freq:
            return self.freq < other.freq   # lower freq pops first
        return self.word > other.word       # larger word pops first


class Solution:
    def topKFrequent(self, words, k):
        counts = Counter(words)
        heap = []
        for word, freq in counts.items():
            heapq.heappush(heap, _Item(word, freq))
            if len(heap) > k:
                heapq.heappop(heap)
        result = [heapq.heappop(heap).word for _ in range(len(heap))]
        result.reverse()
        return result
```

## unittest test cases

```python
import unittest


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
        self.assertEqual(self.sol.topKFrequent(words, 2), ["a", "b"])

    def test_single_word(self):
        self.assertEqual(self.sol.topKFrequent(["hello"], 1), ["hello"])

    def test_frequency_dominates_over_alpha(self):
        words = ["aaa", "bbb", "bbb", "ccc", "ccc", "ccc"]
        self.assertEqual(self.sol.topKFrequent(words, 1), ["ccc"])
```

## Interview tips

- The sort key `(-count, word)` captures both rules at once: highest frequency first, ties broken by smallest word.
- `heapq.nsmallest` with that key is the cleanest line and runs in `O(m log k)`.
- To avoid the key trick, build a max-heap of `(-count, word)` and pop `k` times — remember Python heaps are min-heaps, so negate the count.
- The size-`k` min-heap with a custom `__lt__` achieves the `O(n log k)` follow-up but is fiddly: the tie-break must be inverted so the word that should be **dropped** (larger) compares as smaller.
- Watch the tie-break direction carefully — it's the most common bug in this problem.
