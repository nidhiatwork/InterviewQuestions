"""
LeetCode #950 - Reveal Cards In Increasing Order  (Queue - Medium)
URL: https://leetcode.com/problems/reveal-cards-in-increasing-order/

Problem
-------
You are given an integer array deck. There is a deck of cards where every card
has a unique integer. You can order the deck however you want.

Initially, all cards start face down in one deck. Repeatedly do this:

1. Take the top card, reveal it, and remove it from the deck.
2. If there are still cards left, take the next top card and move it to the
   bottom of the deck.
3. Repeat until all cards are revealed.

Return an ordering of the deck that reveals the cards in increasing order.

Examples
--------
1) Input:  deck = [17,13,11,2,3,5,7]
   Output: [2,13,3,11,5,17,7]
   Explanation: Revealed order is [2,3,5,7,11,13,17].

2) Input:  deck = [1,1000]
   Output: [1,1000]

3) Input:  deck = [4]
   Output: [4]

Constraints
-----------
- 1 <= deck.length <= 1000
- 1 <= deck[i] <= 10^6
- All values in deck are unique.

Run
---
    python 2026-06-08-reveal-cards-in-increasing-order.py -v
"""

from collections import deque
import unittest


class Solution:
    def deckRevealedIncreasing(self, deck):
        raise NotImplementedError("Implement deckRevealedIncreasing")


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

    def test_already_sorted_deck(self):
        self.assertRevealsIncreasing([1, 2, 3, 4, 5, 6])

    def test_reverse_sorted_deck(self):
        self.assertRevealsIncreasing([9, 8, 7, 6, 5])

    def test_large_values(self):
        self.assertRevealsIncreasing([1000000, 1, 500000, 250000])

    def test_does_not_mutate_input_require_order(self):
        deck = [6, 2, 9, 1, 4]
        self.assertRevealsIncreasing(deck)
        self.assertEqual(deck, [6, 2, 9, 1, 4])


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  - peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
Simulate the reveal process on positions, not on card values.

The smallest card must be revealed first, the second-smallest card must be
revealed second, and so on. If we know which original deck position is revealed
at each step, we can place the sorted cards into those positions.

1. Sort the cards.
2. Put indexes [0, 1, ..., n - 1] into a queue.
3. For each card in sorted order:
   - Pop the next index; place the current card there.
   - If indexes remain, pop the next index and push it to the back, matching the
     "move top card to bottom" rule.
4. Return the filled answer array.

This is easier than trying to reason backward with card values. The queue
faithfully models which positions are revealed by the process.

Complexity
----------
- Time:  O(n log n), for sorting. The queue simulation is O(n).
- Space: O(n), for the answer array and index queue.

Python solution
---------------
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

Interview tips
--------------
- Say that the queue stores positions, not cards.
- Sorting tells us the desired reveal order; the queue tells us where each card
  must be placed to achieve that order.
- Do not simulate with the unsorted deck values directly; that makes the logic
  harder than necessary.
- For n = 1, the queue move step should be skipped because no card remains.
- A valid alternative is reverse simulation from largest to smallest, but the
  index-queue version is usually easier to explain.
"""
