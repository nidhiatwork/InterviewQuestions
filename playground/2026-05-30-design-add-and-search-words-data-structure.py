"""LeetCode #211 — Design Add and Search Words Data Structure  (Trie · Medium)

URL: https://leetcode.com/problems/design-add-and-search-words-data-structure/

Problem
-------
Design a data structure that supports adding new words and finding whether
a string matches any previously added word.

Implement the WordDictionary class:
  WordDictionary()          Initializes the object.
  void addWord(word)        Adds word to the data structure.
  bool search(word)         Returns True if there is any string in the
                            structure that matches word. word may contain
                            the dot character '.' which can match any
                            single letter.

Examples
--------
  wd = WordDictionary()
  wd.addWord("bad")
  wd.addWord("dad")
  wd.addWord("mad")
  wd.search("pad")  -> False
  wd.search("bad")  -> True
  wd.search(".ad")  -> True
  wd.search("b..")  -> True

Constraints
-----------
  1 <= word.length <= 25
  word in addWord consists of lowercase English letters.
  word in search consists of '.' or lowercase English letters.
  There will be at most 2 dots in word for search queries.
  At most 10^4 calls in total to addWord and search.

Run
---
  python 2026-05-30-design-add-and-search-words-data-structure.py -v
"""

import unittest


class WordDictionary:
    def __init__(self):
        raise NotImplementedError("Implement __init__")

    def addWord(self, word):
        raise NotImplementedError("Implement addWord")

    def search(self, word):
        raise NotImplementedError("Implement search")


# ----------------------------- tests -----------------------------

class TestWordDictionary(unittest.TestCase):
    def test_example(self):
        wd = WordDictionary()
        wd.addWord("bad")
        wd.addWord("dad")
        wd.addWord("mad")
        self.assertFalse(wd.search("pad"))
        self.assertTrue(wd.search("bad"))
        self.assertTrue(wd.search(".ad"))
        self.assertTrue(wd.search("b.."))

    def test_empty_dictionary(self):
        wd = WordDictionary()
        self.assertFalse(wd.search("a"))
        self.assertFalse(wd.search("."))

    def test_single_letter(self):
        wd = WordDictionary()
        wd.addWord("a")
        self.assertTrue(wd.search("a"))
        self.assertTrue(wd.search("."))
        self.assertFalse(wd.search("b"))
        self.assertFalse(wd.search(".."))   # length must match

    def test_length_must_match_exactly(self):
        wd = WordDictionary()
        wd.addWord("hello")
        self.assertFalse(wd.search("hell"))
        self.assertFalse(wd.search("helloo"))
        self.assertTrue(wd.search("hello"))
        self.assertTrue(wd.search("h.llo"))
        self.assertTrue(wd.search("....."))

    def test_prefix_only_does_not_match(self):
        wd = WordDictionary()
        wd.addWord("apple")
        self.assertFalse(wd.search("app"))
        self.assertTrue(wd.search("apple"))

    def test_duplicate_adds_are_safe(self):
        wd = WordDictionary()
        wd.addWord("dog")
        wd.addWord("dog")
        self.assertTrue(wd.search("dog"))
        self.assertTrue(wd.search("d.g"))

    def test_dot_at_start_and_end(self):
        wd = WordDictionary()
        wd.addWord("cat")
        wd.addWord("car")
        wd.addWord("cup")
        self.assertTrue(wd.search(".at"))
        self.assertTrue(wd.search("ca."))
        self.assertTrue(wd.search("..."))
        self.assertFalse(wd.search("....."))   # length mismatch
        self.assertFalse(wd.search("dog"))

    def test_overlapping_words(self):
        wd = WordDictionary()
        for w in ["at", "and", "an", "add", "a", "bat"]:
            wd.addWord(w)
        self.assertTrue(wd.search("a"))
        self.assertTrue(wd.search(".at"))
        self.assertTrue(wd.search("an."))
        self.assertFalse(wd.search("anx"))
        self.assertFalse(wd.search("addd"))

    def test_two_dots(self):
        wd = WordDictionary()
        wd.addWord("abcd")
        wd.addWord("axcd")
        wd.addWord("aycd")
        self.assertTrue(wd.search("a.cd"))
        self.assertTrue(wd.search("a..d"))
        self.assertFalse(wd.search("a..x"))


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  — peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
The wildcard '.' makes a plain hash-set-of-words solution slow: for a search
with k dots and N stored words you'd have to scan all words of matching
length. A trie collapses shared prefixes so the wildcard fans out only into
the children that actually exist.

Trie layout:
  - Each node = dict mapping char -> child node.
  - Each node has an `is_end` flag set True for the last char of an inserted
    word. (Length matching falls out for free — search returns True only
    when we land on an `is_end` node at the exact end of the query.)

addWord: walk/insert one node per char, flip `is_end` at the last char.

search: DFS over the trie consuming the query left to right.
  - At position i with char c = word[i]:
      * if c == '.', recurse into every child of the current node.
      * else, recurse only into node.children[c] if it exists.
  - Base case: i == len(word) -> return current.is_end.

The "at most 2 dots" constraint guarantees the wildcard branching factor
is bounded — overall complexity stays close to O(L) per query.

Complexity
----------
Let L = word length, A = alphabet size (26), N = number of stored words.
- addWord: O(L) time, O(L * A) extra space worst case (new branch).
- search worst case (all dots): O(A^d * L) where d = number of dots.
- With d <= 2 (given): essentially O(L) amortized.
- Space: O(total characters across all inserted words).

Python solution
---------------
class WordDictionary:
    def __init__(self):
        self.children = {}
        self.is_end = False

    def addWord(self, word):
        node = self
        for ch in word:
            if ch not in node.children:
                node.children[ch] = WordDictionary()
            node = node.children[ch]
        node.is_end = True

    def search(self, word):
        def dfs(node, i):
            if i == len(word):
                return node.is_end
            ch = word[i]
            if ch == '.':
                return any(dfs(child, i + 1) for child in node.children.values())
            child = node.children.get(ch)
            return child is not None and dfs(child, i + 1)

        return dfs(self, 0)

# Memory-tighter variant: separate Node class so the WordDictionary itself
# only holds a root pointer — same logic, slightly cleaner naming.
#
# class _Node:
#     __slots__ = ("children", "is_end")
#     def __init__(self):
#         self.children = {}
#         self.is_end = False
#
# class WordDictionary:
#     def __init__(self):
#         self.root = _Node()
#     def addWord(self, word):
#         node = self.root
#         for ch in word:
#             node = node.children.setdefault(ch, _Node())
#         node.is_end = True
#     def search(self, word):
#         def dfs(node, i):
#             if i == len(word):
#                 return node.is_end
#             ch = word[i]
#             if ch == '.':
#                 return any(dfs(child, i+1) for child in node.children.values())
#             nxt = node.children.get(ch)
#             return nxt is not None and dfs(nxt, i+1)
#         return dfs(self.root, 0)

Interview tips
--------------
- Lead with WHY a trie: shared prefixes make the wildcard scan branch only
  into nodes that actually exist, instead of all stored words.
- Use a dict for children, not a fixed-size array of 26 — Python dict is
  fast enough and skips the empty-slot overhead. (For a C++/Java answer, a
  size-26 array trades memory for cache locality; mention the trade-off.)
- The `is_end` flag is non-negotiable. Without it you can't distinguish
  "this string was added" from "this string is a prefix of something added"
  -> "apple" stored, search("app") must be False.
- Length matching is implicit — the recursion bottoms out at i == len(word)
  and checks is_end. Don't add extra length bookkeeping.
- Microsoft follow-up: "support delete." Either reference-count nodes on
  the way in and decrement on delete, or do a recursive delete that prunes
  empty subtrees on unwind. Mention; don't implement unless asked.
- Another classic follow-up: "what if a query can have many dots?" Now you
  want to bound branching — e.g., precompute word-length buckets and skip
  any subtree whose remaining depth can't match. Wave at it; only sketch
  the code if pushed.
"""
