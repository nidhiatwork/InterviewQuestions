"""
LeetCode #649 - Dota2 Senate  (Queue - Medium)
URL: https://leetcode.com/problems/dota2-senate/

Problem
-------
In the world of Dota2, there are two parties: the Radiant and the Dire.

The Dota2 senate consists of senators coming from two parties. Now the Senate
wants to decide on a change in the Dota2 game. The voting for this change is a
round-based procedure. In each round, each senator can exercise one of the two
rights:
  - Ban one senator's right: A senator can make another senator lose all his
    rights in this and all the following rounds.
  - Announce the victory: If this senator found the senators who still have
    rights to vote are all from the same party, he can announce the victory and
    decide on the change in the game.

Given a string senate representing each senator's party belonging. The character
'R' and 'D' represent the Radiant party and the Dire party. Then if there are n
senators, the size of the given string will be n.

The round-based procedure starts from the first senator to the last senator in
the given order. This procedure will last until the end of voting. All the
senators who have lost their rights will be skipped during the procedure.

Suppose every senator is smart enough and will play the best strategy for his
own party. Predict which party will finally announce the victory and change the
Dota2 game. The output should be "Radiant" or "Dire".

Examples
--------
1) Input:  senate = "RD"
   Output: "Radiant"
   Explanation: The first senator comes from Radiant and he can just ban the next
   senator's right in round 1. And the second senator can't exercise any right
   anymore since his right has been banned. And in round 2, the first senator can
   just announce the victory since he is the only guy in the senate who can vote.

2) Input:  senate = "RDD"
   Output: "Dire"
   Explanation:
   - Round 1: R bans D at index 1; D at index 2 bans R at index 0.
   - Round 2: only D at index 2 remains, so Dire announces victory.

Constraints
-----------
- 1 <= senate.length <= 10^4
- senate[i] is either 'R' or 'D'.

Run
---
    python 2026-06-26-dota2-senate.py -v
"""

from collections import deque
import unittest


class Solution:
    def predictPartyVictory(self, senate):
        raise NotImplementedError("Implement predictPartyVictory")


class TestPredictPartyVictory(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1(self):
        self.assertEqual(self.sol.predictPartyVictory("RD"), "Radiant")

    def test_example_2(self):
        self.assertEqual(self.sol.predictPartyVictory("RDD"), "Dire")

    def test_single_radiant(self):
        self.assertEqual(self.sol.predictPartyVictory("R"), "Radiant")

    def test_single_dire(self):
        self.assertEqual(self.sol.predictPartyVictory("D"), "Dire")

    def test_all_radiant(self):
        self.assertEqual(self.sol.predictPartyVictory("RRRR"), "Radiant")

    def test_all_dire(self):
        self.assertEqual(self.sol.predictPartyVictory("DDDD"), "Dire")

    def test_radiant_majority(self):
        self.assertEqual(self.sol.predictPartyVictory("RRD"), "Radiant")

    def test_equal_radiant_first(self):
        # equal counts, Radiant acts first each round -> Radiant wins
        self.assertEqual(self.sol.predictPartyVictory("RDRD"), "Radiant")

    def test_dire_first_equal(self):
        self.assertEqual(self.sol.predictPartyVictory("DRDR"), "Dire")


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  - peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
Simulate the rounds with two queues of indices, one per party. The smaller index
in each round acts first and bans the opponent who is next in line.

Setup:
  - Put the indices of all 'R' senators into queue `radiant`, and all 'D'
    senators into queue `dire`, preserving original order.

Each step: pop the front of both queues - these are the two senators whose turn
comes earliest among those still active. The one with the SMALLER index acts
first and bans the other (so the other does not get re-queued). The winner
survives and goes to the back of the line for the NEXT round, which we model by
re-adding its index + n (so it sorts after everyone in the current round).

Repeat until one queue is empty. The party whose queue still has senators wins.

Why index + n: adding n pushes the surviving senator past all current-round
indices, preserving correct ordering across rounds without rebuilding queues.

Complexity
----------
- Time:  O(n), each senator is processed a constant number of times per
  effective round; total work is linear because each ban removes one senator.
- Space: O(n) for the two queues.

Python solution
---------------
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
                radiant.append(r + n)   # R acts first, bans D; R survives next round
            else:
                dire.append(d + n)      # D acts first, bans R; D survives next round

        return "Radiant" if radiant else "Dire"

Interview tips
--------------
- The key insight: the senator with the smaller current index always acts first,
  so compare the two front indices and let the smaller one ban the other.
- Re-enqueue the survivor as index + n to place it after everyone in this round -
  a clean trick to keep ordering without tracking explicit round numbers.
- This is greedy and optimal: each senator bans the nearest upcoming opponent,
  which is the strongest move for their party.
- Total time is O(n) because every comparison removes exactly one senator from
  the game permanently.
- Edge cases: a single senator, or all senators from one party, return that party
  immediately.
"""
