# LeetCode #950 - Reveal Cards In Increasing Order

**Data structure:** Queue  
**Difficulty:** Medium  
**URL:** https://leetcode.com/problems/reveal-cards-in-increasing-order/

## Problem

You are given an integer array `deck` with unique values. You may order the deck however you want.

Starting from the top of the deck, repeatedly:

1. Reveal the top card and remove it.
2. If cards remain, move the next top card to the bottom.
3. Continue until every card is revealed.

Return an ordering of the deck such that the revealed cards appear in increasing order.

## Examples

```text
Input: deck = [17,13,11,2,3,5,7]
Output: [2,13,3,11,5,17,7]
```

```text
Input: deck = [1,1000]
Output: [1,1000]
```

```text
Input: deck = [4]
Output: [4]
```

## Constraints

- `1 <= deck.length <= 1000`
- `1 <= deck[i] <= 10^6`
- All values in `deck` are unique.

## Approach

Simulate the reveal process on indexes instead of card values.

The sorted cards are the order we want to reveal: smallest first, then next-smallest, and so on. The only question is which original position is revealed at each step.

1. Sort `deck`.
2. Put indexes `0..n-1` into a queue.
3. For each card in sorted order, pop the next index and place that card there.
4. If indexes remain, pop the next index and append it to the back to simulate moving the top card to the bottom.

The queue models the reveal order of positions, so filling those positions with sorted values produces the required deck.

**Complexity**

- Time: `O(n log n)` for sorting
- Space: `O(n)` for the answer and queue

## Python solution

```python
from collections import deque


class Solution:
    def deckRevealedIncreasing(self, deck):
        indexes = deque(range(len(deck)))
        answer = [0] * len(deck)

        for card in sorted(deck):
            reveal_at = indexes.popleft()
            answer[reveal_at] = card
            if indexes:
                indexes.append(indexes.popleft())

        return answer
```

## unittest test cases

```python
import unittest
from collections import deque


def reveal_order(deck):
    q = deque(deck)
    revealed = []
    while q:
        revealed.append(q.popleft())
        if q:
            q.append(q.popleft())
    return revealed


class TestRevealCardsIncreasing(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def assertRevealsIncreasing(self, deck):
        result = self.sol.deckRevealedIncreasing(deck[:])
        self.assertEqual(sorted(result), sorted(deck))
        self.assertEqual(reveal_order(result), sorted(deck))

    def test_example_1(self):
        self.assertEqual(
            self.sol.deckRevealedIncreasing([17, 13, 11, 2, 3, 5, 7]),
            [2, 13, 3, 11, 5, 17, 7],
        )

    def test_two_cards(self):
        self.assertEqual(self.sol.deckRevealedIncreasing([1, 1000]), [1, 1000])

    def test_single_card(self):
        self.assertEqual(self.sol.deckRevealedIncreasing([4]), [4])

    def test_unsorted_small_deck(self):
        self.assertRevealsIncreasing([10, 1, 7, 3])
```

## Interview tips

- The queue stores indexes, not card values.
- Sorting gives the target reveal sequence; queue simulation gives the target positions.
- Handle the single-card case by checking whether the queue still has indexes before rotating.
- If asked for another approach, describe reverse simulation from largest to smallest.
- Verify by manually simulating `[2,13,3,11,5,17,7]` to show it reveals `[2,3,5,7,11,13,17]`.
