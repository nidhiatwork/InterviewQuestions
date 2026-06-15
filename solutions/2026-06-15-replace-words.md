# LeetCode #648 - Replace Words

**Data structure:** Trie  
**Difficulty:** Medium  
**URL:** https://leetcode.com/problems/replace-words/

## Problem

In English, a **root** can be followed by another word to form a longer **derivative** — e.g. the root `"help"` + `"ful"` forms `"helpful"`.

Given a dictionary of roots and a sentence of space-separated words, replace every derivative in the sentence with the root forming it. If a derivative can be formed by more than one root, use the **shortest** root.

Return the sentence after replacement.

## Examples

```text
Input: dictionary = ["cat","bat","rat"], sentence = "the cattle was rattled by the battery"
Output: "the cat was rat by the bat"
```

```text
Input: dictionary = ["a","b","c"], sentence = "aadsfasf absbs bbab cadsfafs"
Output: "a a b c"
```

## Constraints

- `1 <= dictionary.length <= 1000`, each root `1..100` lowercase letters.
- `1 <= sentence.length <= 10^6`, lowercase letters and spaces only.
- `1..1000` words, separated by exactly one space, no leading/trailing spaces.

## Approach

Build a trie of the roots, then for each word walk the trie to find the shortest matching prefix.

1. Insert every root into a trie, marking the final node of each root as a word end.
2. For each word in the sentence, descend the trie character by character:
   - If the next character is missing, no root is a prefix → keep the original word.
   - If we reach a node marked as a word end, we found the shortest root (shortest because we stop at the **first** end encountered) → replace the word with the accumulated prefix.
3. Join the resulting words with single spaces.

The trie gives `O(L)` prefix lookup per word, and stopping at the first word-end node naturally yields the shortest root.

**Complexity**

- Time: `O(total root length + total sentence length)`
- Space: `O(total root length)` for the trie

## Python solution

```python
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
```

## unittest test cases

```python
import unittest


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
        self.assertEqual(self.sol.replaceWords(dictionary, sentence), "a a b c")

    def test_shortest_root_wins(self):
        dictionary = ["cat", "ca"]
        sentence = "catastrophe"
        self.assertEqual(self.sol.replaceWords(dictionary, sentence), "ca")

    def test_no_matching_root(self):
        dictionary = ["xyz"]
        sentence = "hello world"
        self.assertEqual(self.sol.replaceWords(dictionary, sentence), "hello world")

    def test_root_longer_than_word(self):
        dictionary = ["longer"]
        sentence = "long"
        self.assertEqual(self.sol.replaceWords(dictionary, sentence), "long")
```

## Interview tips

- Stopping at the **first** word-end node during descent guarantees the shortest root — no need to compare candidate lengths.
- A hash-set-of-prefixes approach also works (try every prefix from shortest), but the trie is cleaner and avoids rebuilding prefix strings.
- Watch the no-match case: if a character is missing or no end node is hit, keep the original word.
- Splitting on spaces and re-joining with a single space is safe given the single-space guarantee.
- The trie scales better than re-scanning the dictionary per word, especially for large dictionaries.
