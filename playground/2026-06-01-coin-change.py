"""LeetCode #322 — Coin Change  (Array · Medium)

URL: https://leetcode.com/problems/coin-change/

Problem
-------
You are given an integer array coins representing coins of different
denominations and an integer amount representing a total amount of money.

Return the fewest number of coins that you need to make up that amount.
If that amount of money cannot be made up by any combination of the coins,
return -1.

You may assume that you have an infinite number of each kind of coin.

Examples
--------
  coins = [1,2,5], amount = 11    ->  3   (11 = 5 + 5 + 1)
  coins = [2], amount = 3         -> -1
  coins = [1], amount = 0         ->  0
  coins = [186,419,83,408], amount = 6249 -> 20

Constraints
-----------
  1 <= coins.length <= 12
  1 <= coins[i] <= 2^31 - 1
  0 <= amount <= 10^4

Run
---
  python 2026-06-01-coin-change.py -v
"""

import unittest


class Solution:
    def coinChange(self, coins, amount):
        raise NotImplementedError("Implement coinChange")


# ----------------------------- tests -----------------------------

class TestCoinChange(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1(self):
        self.assertEqual(self.sol.coinChange([1, 2, 5], 11), 3)

    def test_example_2_impossible(self):
        self.assertEqual(self.sol.coinChange([2], 3), -1)

    def test_zero_amount(self):
        self.assertEqual(self.sol.coinChange([1], 0), 0)
        self.assertEqual(self.sol.coinChange([7, 13], 0), 0)

    def test_amount_equals_coin(self):
        self.assertEqual(self.sol.coinChange([1, 5, 10], 10), 1)

    def test_only_ones(self):
        self.assertEqual(self.sol.coinChange([1], 7), 7)

    def test_large_coin_only_does_not_fit(self):
        self.assertEqual(self.sol.coinChange([5, 10], 3), -1)

    def test_greedy_would_be_wrong(self):
        # Greedy from biggest (4 then 1+1+1) gives 4 coins; optimal is 3+3 = 2.
        self.assertEqual(self.sol.coinChange([1, 3, 4], 6), 2)

    def test_microsoft_style_large(self):
        # 6249 = 419*14 + 83*4 + 1*... actually best uses 419s + smaller.
        # Verified answer per LeetCode: 20.
        self.assertEqual(self.sol.coinChange([186, 419, 83, 408], 6249), 20)

    def test_amount_one(self):
        self.assertEqual(self.sol.coinChange([1, 2, 5], 1), 1)
        self.assertEqual(self.sol.coinChange([2, 5], 1), -1)


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  — peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
Reframe the problem as shortest path in an unweighted graph:

  - Nodes      = amounts 0, 1, 2, ..., amount.
  - Start node = amount   (we want to drain it to 0).
  - Edges      = from node `n`, you can move to `n - c` for any coin c
                 with c <= n. Each edge costs exactly 1 coin (1 hop).
  - Goal node  = 0.

Because every edge has weight 1, the fewest coins = fewest hops = the
shortest path. Shortest path in an unweighted graph is exactly BFS from
the goal-or-source, level by level. The first time we visit 0, the BFS
level is the answer; if we exhaust the queue without ever reaching 0,
return -1.

Why this beats brute force: BFS visits each amount at most once, and
processes each (amount, coin) edge once. A `seen` set keeps us from
re-expanding amounts we've already reached at a smaller depth.

Why this beats greedy: greedy from the biggest coin fails on coin sets
like [1, 3, 4] / amount 6 — it would pick 4 + 1 + 1 (3 coins), missing
3 + 3 (2 coins). BFS explores all coin choices at each level in lockstep,
so the first hit is provably optimal.

A streaming alternative (same big-O) walks amounts 1..target left to
right and at each step asks "from which earlier amount could I reach
here in one coin hop?" — keep the minimum. That's also non-recursive,
non-DP-language, just iterative relaxation.

Complexity
----------
Let A = amount, C = number of coins.
- Time:  O(A * C)   each amount enqueued once, scanned against C coins
- Space: O(A)       visited set + BFS queue

Python solution
---------------
from collections import deque

class Solution:
    def coinChange(self, coins, amount):
        if amount == 0:
            return 0
        # BFS from `amount` down to 0; edges cost 1 coin each.
        seen = {amount}
        queue = deque([amount])
        steps = 0
        while queue:
            steps += 1
            for _ in range(len(queue)):
                node = queue.popleft()
                for c in coins:
                    nxt = node - c
                    if nxt == 0:
                        return steps
                    if nxt > 0 and nxt not in seen:
                        seen.add(nxt)
                        queue.append(nxt)
        return -1

# Iterative-relaxation alternative (also non-DP framing):
#
# class Solution:
#     def coinChange(self, coins, amount):
#         INF = amount + 1                  # sentinel = "unreachable"
#         fewest = [0] + [INF] * amount     # fewest[a] = min coins to make a
#         for a in range(1, amount + 1):
#             for c in coins:
#                 if c <= a and fewest[a - c] + 1 < fewest[a]:
#                     fewest[a] = fewest[a - c] + 1
#         return fewest[amount] if fewest[amount] != INF else -1

Interview tips
--------------
- Open by reframing: "fewest coins" = "shortest path in an unweighted
  graph where amounts are nodes and each coin is a 1-hop edge." That
  single sentence picks the algorithm — BFS — for you.
- Explicitly defuse greedy. The interviewer often expects you to *try*
  greedy and then explain why it fails (the [1,3,4] / 6 counterexample
  is the canonical one). Showing you know why greedy doesn't work is
  half the signal.
- BFS-from-amount-toward-0 is slightly cleaner than BFS-from-0-up: the
  `nxt == 0` check is right at the edge expansion, no off-by-one to
  worry about.
- The `seen` set is load-bearing. Without it the queue blows up on big
  amount values because we'd re-enqueue the same node from every coin.
- Microsoft follow-up: "now return one valid coin set." Cache a `parent`
  pointer alongside `seen` (parent[next] = (node, coin)) and walk it
  back from 0 once you hit. O(amount/min_coin) extra to reconstruct.
- Bigger follow-up: "what if a coin can only be used once" — that's the
  subset-sum / knapsack variant; the BFS reframing still works but the
  state becomes (amount, frozenset_of_used_coins), so size matters. Wave
  at it; only sketch if pushed.
- Don't say the words "dp", "memoization", "recurrence", or "subproblem"
  in the room — frame everything as graph search / iterative relaxation
  / shortest path. Same big-O, cleaner story.
"""
