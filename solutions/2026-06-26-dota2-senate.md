# LeetCode #649 - Dota2 Senate

**Data structure:** Queue  
**Difficulty:** Medium  
**URL:** https://leetcode.com/problems/dota2-senate/

## Problem

Senators come from two parties: Radiant (`'R'`) and Dire (`'D'`). Voting is round-based; each active senator, in order, may either **ban** one opponent (removing their rights for this and all future rounds) or **announce victory** if all remaining active senators are from their party.

Given a string `senate`, every senator plays optimally for their party. Return which party wins: `"Radiant"` or `"Dire"`.

## Examples

```text
Input: senate = "RD"
Output: "Radiant"
```

```text
Input: senate = "RDD"
Output: "Dire"
```

## Constraints

- `1 <= senate.length <= 10^4`
- `senate[i]` is `'R'` or `'D'`.

## Approach

Simulate the rounds with two queues of indices, one per party. The smaller index in each round acts first and bans the opponent next in line.

**Setup:** put indices of all `'R'` senators into queue `radiant` and all `'D'` into `dire`, preserving order.

**Each step:** pop the front of both queues — the two senators whose turn comes earliest among those still active. The one with the **smaller index** acts first and bans the other (the other is not re-queued). The survivor goes to the back for the next round, modeled by re-adding its `index + n` (so it sorts after everyone in the current round).

Repeat until one queue is empty; the non-empty party wins.

Adding `n` pushes the survivor past all current-round indices, preserving cross-round order without rebuilding queues.

**Complexity**

- Time: `O(n)` — each ban permanently removes one senator
- Space: `O(n)` for the two queues

## Python solution

```python
from collections import deque


class Solution:
    def predictPartyVictory(self, senate):
        n = len(senate)
        radiant = deque(i for i, c in enumerate(senate) if c == 'R')
        dire = deque(i for i, c in enumerate(senate) if c == 'D')

        while radiant and dire:
            r = radiant.popleft()
            d = dire.popleft()
            if r < d:
                radiant.append(r + n)   # R acts first, bans D
            else:
                dire.append(d + n)      # D acts first, bans R

        return "Radiant" if radiant else "Dire"
```

## unittest test cases

```python
import unittest


class TestPredictPartyVictory(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1(self):
        self.assertEqual(self.sol.predictPartyVictory("RD"), "Radiant")

    def test_example_2(self):
        self.assertEqual(self.sol.predictPartyVictory("RDD"), "Dire")

    def test_all_radiant(self):
        self.assertEqual(self.sol.predictPartyVictory("RRRR"), "Radiant")

    def test_equal_radiant_first(self):
        self.assertEqual(self.sol.predictPartyVictory("RDRD"), "Radiant")

    def test_dire_first_equal(self):
        self.assertEqual(self.sol.predictPartyVictory("DRDR"), "Dire")
```

## Interview tips

- Key insight: the senator with the smaller current index always acts first, so compare the two front indices and let the smaller one ban the other.
- Re-enqueue the survivor as `index + n` to place it after everyone in this round — a clean trick to keep ordering without explicit round numbers.
- It's greedy and optimal: each senator bans the nearest upcoming opponent, the strongest move for their party.
- Total time is `O(n)` because every comparison permanently removes one senator.
- Edge cases: a single senator, or all from one party, return that party immediately.
