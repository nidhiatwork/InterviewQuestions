"""LeetCode #208 — Implement Trie (Prefix Tree)  (Trie · Medium)

URL: https://leetcode.com/problems/implement-trie-prefix-tree/

Problem
-------
Implement a Trie with:
  Trie()                  -> initialize
  insert(word)            -> insert a word
  search(word)            -> True iff exact word was inserted before
  startsWith(prefix)      -> True iff any inserted word has this prefix

Constraints
-----------
  1 <= word.length, prefix.length <= 2000
  Lowercase English letters only.
  At most 3*10^4 calls.

Run
---
  python 2026-05-16-implement-trie-prefix-tree.py -v
"""

import unittest


class Trie:
    def __init__(self):
        raise NotImplementedError("Implement __init__")

    def insert(self, word):
        raise NotImplementedError("Implement insert")

    def search(self, word):
        raise NotImplementedError("Implement search")

    def startsWith(self, prefix):
        raise NotImplementedError("Implement startsWith")


# ----------------------------- tests -----------------------------

class TestTrie(unittest.TestCase):
    def test_leetcode_example(self):
        trie = Trie()
        trie.insert("apple")
        self.assertTrue(trie.search("apple"))
        self.assertFalse(trie.search("app"))
        self.assertTrue(trie.startsWith("app"))
        trie.insert("app")
        self.assertTrue(trie.search("app"))

    def test_empty_trie(self):
        trie = Trie()
        self.assertFalse(trie.search("a"))
        self.assertFalse(trie.startsWith("a"))

    def test_prefix_not_a_word(self):
        trie = Trie()
        trie.insert("application")
        self.assertTrue(trie.startsWith("app"))
        self.assertTrue(trie.startsWith("appl"))
        self.assertFalse(trie.search("app"))
        self.assertFalse(trie.search("appl"))
        self.assertTrue(trie.search("application"))

    def test_duplicate_inserts(self):
        trie = Trie()
        trie.insert("dog")
        trie.insert("dog")
        self.assertTrue(trie.search("dog"))
        self.assertFalse(trie.search("do"))
        self.assertTrue(trie.startsWith("do"))

    def test_shared_branches(self):
        trie = Trie()
        for w in ("car", "cart", "care", "cargo", "cat"):
            trie.insert(w)
        for w in ("car", "cart", "care", "cargo", "cat"):
            self.assertTrue(trie.search(w), w)
        self.assertFalse(trie.search("ca"))
        self.assertFalse(trie.search("card"))
        self.assertTrue(trie.startsWith("car"))
        self.assertTrue(trie.startsWith("ca"))
        self.assertFalse(trie.startsWith("cb"))

    def test_long_word_and_unrelated_prefix(self):
        trie = Trie()
        trie.insert("a" * 1000)
        self.assertTrue(trie.search("a" * 1000))
        self.assertTrue(trie.startsWith("a" * 999))
        self.assertFalse(trie.search("a" * 999))
        self.assertFalse(trie.search("a" * 1001))
        self.assertFalse(trie.startsWith("b"))


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  — peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
Each node holds a dict `children` mapping next char -> child node, plus a
boolean `is_end` marking whether a complete word terminates there.

- insert: walk char-by-char, creating missing children; mark final node is_end
- search: walk; missing char -> False; else return terminal node's is_end
- startsWith: same walk as search; final answer is "did we reach the end of
  the prefix?" — is_end does not matter

A 26-slot array is slightly faster than a dict but less general.

Complexity
----------
- insert / search / startsWith:  O(L) where L = length of word/prefix
- Space: O(total chars inserted) worst case

Python solution
---------------
class _Node:
    __slots__ = ('children', 'is_end')
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = _Node()

    def insert(self, word):
        node = self.root
        for ch in word:
            nxt = node.children.get(ch)
            if nxt is None:
                nxt = _Node()
                node.children[ch] = nxt
            node = nxt
        node.is_end = True

    def _walk(self, s):
        node = self.root
        for ch in s:
            node = node.children.get(ch)
            if node is None:
                return None
        return node

    def search(self, word):
        node = self._walk(word)
        return node is not None and node.is_end

    def startsWith(self, prefix):
        return self._walk(prefix) is not None

Interview tips
--------------
- Mention the dict-vs-fixed-array tradeoff: array is faster + lower memory
  for a bounded alphabet (lowercase a-z).
- search and startsWith differ by ONE LINE: search requires is_end,
  startsWith does not. Factor the shared walk into a helper.
- Complexity is in terms of L (word length), not n (number of words). The
  distinction matters when discussing autocomplete latency at scale.
"""
