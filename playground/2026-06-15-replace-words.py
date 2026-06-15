"""
LeetCode #648 - Replace Words  (Trie - Medium)
URL: https://leetcode.com/problems/replace-words/

Problem
-------
In English, we have a concept called root, which can be followed by some other
word to form another longer word - let's call this word a derivative. For
example, when the root "help" is followed by the word "ful", we can form a
derivative "helpful".

Given a dictionary consisting of many roots and a sentence consisting of words
separated by spaces, replace all the derivatives in the sentence with the root
forming it. If a derivative can be replaced by more than one root, replace it
with the root that has the shortest length.

Return the sentence after the replacement.

Examples
--------
1) Input:  dictionary = ["cat","bat","rat"],
           sentence = "the cattle was rattled by the battery"
   Output: "the cat was rat by the bat"

2) Input:  dictionary = ["a","b","c"],
           sentence = "aadsfasf absbs bbab cadsfafs"
   Output: "a a b c"

Constraints
-----------
- 1 <= dictionary.length <= 1000
- 1 <= dictionary[i].length <= 100
- dictionary[i] consists of only lowercase letters.
- 1 <= sentence.length <= 10^6
- sentence consists of only lowercase letters and spaces.
- The number of words in sentence is in the range [1, 1000].
- Every two consecutive words in sentence will be separated by exactly one space.
- sentence does not have leading or trailing spaces.

Run
---
    python 2026-06-15-replace-words.py -v
"""

import unittest


class Solution:
    def replaceWords(self, dictionary, sentence):
        raise NotImplementedError("Implement replaceWords")


class TestReplaceWords(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1(self):
        dictionary = ["cat", "bat", "rat"]
        sentence = "the cattle was rattled by the battery"
        self.assertEqual(
            self.sol.replaceWords(dictionary, sentence),
            "the cat was rat by the bat",
        )

    def test_example_2(self):
        dictionary = ["a", "b", "c"]
        sentence = "aadsfasf absbs bbab cadsfafs"
        self.assertEqual(
            self.sol.replaceWords(dictionary, sentence), "a a b c"
        )

    def test_shortest_root_wins(self):
        dictionary = ["cat", "ca"]
        sentence = "catastrophe"
        self.assertEqual(self.sol.replaceWords(dictionary, sentence), "ca")

    def test_no_matching_root(self):
        dictionary = ["xyz"]
        sentence = "hello world"
        self.assertEqual(self.sol.replaceWords(dictionary, sentence), "hello world")

    def test_word_equals_root(self):
        dictionary = ["dog"]
        sentence = "dog runs"
        self.assertEqual(self.sol.replaceWords(dictionary, sentence), "dog runs")

    def test_root_longer_than_word(self):
        dictionary = ["longer"]
        sentence = "long"
        self.assertEqual(self.sol.replaceWords(dictionary, sentence), "long")

    def test_multiple_replacements(self):
        dictionary = ["se", "th"]
        sentence = "search the theme series"
        self.assertEqual(
            self.sol.replaceWords(dictionary, sentence), "se th th se"
        )


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  - peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
Build a trie of the roots, then for each word walk the trie to find the shortest
matching prefix (root).

1. Insert every root into a trie. Mark the node at the end of each root as a word
   end.
2. For each word in the sentence, walk character by character down the trie:
   - If the next character is missing from the trie, no root is a prefix; keep
     the original word.
   - If we reach a node marked as a word end, we have found the shortest root
     (shortest because we stop at the FIRST end we encounter while descending);
     replace the word with the prefix accumulated so far.
3. Join the resulting words with single spaces.

The trie makes prefix lookup O(L) per word, and because we stop at the first
word-end node, we naturally get the shortest root.

Complexity
----------
- Time:  O(sum of root lengths + total sentence length).
- Space: O(sum of root lengths) for the trie.

Python solution
---------------
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


class Solution:
    def replaceWords(self, dictionary, sentence):
        root = TrieNode()
        for word in dictionary:
            node = root
            for ch in word:
                if ch not in node.children:
                    node.children[ch] = TrieNode()
                node = node.children[ch]
            node.is_end = True

        def shortest_root(word):
            node = root
            prefix = []
            for ch in word:
                if ch not in node.children:
                    return word
                node = node.children[ch]
                prefix.append(ch)
                if node.is_end:
                    return "".join(prefix)
            return word

        return " ".join(shortest_root(w) for w in sentence.split())

Interview tips
--------------
- Stopping at the FIRST word-end node during descent is what guarantees the
  shortest root; no need to compare multiple candidate lengths.
- A hash-set-of-prefixes approach also works (try every prefix of each word from
  shortest), but the trie is cleaner and avoids rebuilding prefix strings.
- Watch the no-match case: if a character is missing or no end node is hit, keep
  the original word unchanged.
- Splitting on spaces and re-joining with a single space is safe because the
  problem guarantees single-space separation and no leading/trailing spaces.
- Mention the trie generalizes to streaming/large dictionaries better than
  repeatedly scanning the dictionary per word.
"""
