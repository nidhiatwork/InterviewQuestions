"""LeetCode #1670 — Design Front Middle Back Queue  (Queue · Medium)

URL: https://leetcode.com/problems/design-front-middle-back-queue/

Problem
-------
Design a queue that supports push and pop operations in the front, middle,
and back positions of the queue.

Implement the FrontMiddleBackQueue class:
  FrontMiddleBackQueue()      -> initializes the queue
  pushFront(val)              -> adds val to the front of the queue
  pushMiddle(val)             -> adds val to the middle of the queue
  pushBack(val)               -> adds val to the back of the queue
  popFront()                  -> removes and returns the front element; -1 if empty
  popMiddle()                 -> removes and returns the middle element; -1 if empty
  popBack()                   -> removes and returns the back element; -1 if empty

When there are two middle position choices, the operation is performed on
the frontmost middle position choice. For example:
  pushMiddle(6) on [1,2,3,4,5]  -> [1,2,6,3,4,5]
  popMiddle()   on [1,2,3,4,5,6] -> returns 3, leaves [1,2,4,5,6]

Examples
--------
  q = FrontMiddleBackQueue()
  q.pushFront(1)    # [1]
  q.pushBack(2)     # [1, 2]
  q.pushMiddle(3)   # [1, 3, 2]
  q.pushMiddle(4)   # [1, 4, 3, 2]
  q.popFront()      # -> 1,  state [4, 3, 2]
  q.popMiddle()     # -> 3,  state [4, 2]
  q.popMiddle()     # -> 4,  state [2]
  q.popBack()       # -> 2,  state []
  q.popFront()      # -> -1, state []

Constraints
-----------
  1 <= val <= 10^9
  At most 1000 calls to each method.

Run
---
  python 2026-05-25-design-front-middle-back-queue.py -v
"""

import unittest
from collections import deque


class FrontMiddleBackQueue:
    def __init__(self):
        raise NotImplementedError("Implement __init__")

    def pushFront(self, val):
        raise NotImplementedError("Implement pushFront")

    def pushMiddle(self, val):
        raise NotImplementedError("Implement pushMiddle")

    def pushBack(self, val):
        raise NotImplementedError("Implement pushBack")

    def popFront(self):
        raise NotImplementedError("Implement popFront")

    def popMiddle(self):
        raise NotImplementedError("Implement popMiddle")

    def popBack(self):
        raise NotImplementedError("Implement popBack")


# ----------------------------- tests -----------------------------

class TestFrontMiddleBackQueue(unittest.TestCase):
    def test_leetcode_example_full_sequence(self):
        q = FrontMiddleBackQueue()
        q.pushFront(1)
        q.pushBack(2)
        q.pushMiddle(3)
        q.pushMiddle(4)
        self.assertEqual(q.popFront(), 1)
        self.assertEqual(q.popMiddle(), 3)
        self.assertEqual(q.popMiddle(), 4)
        self.assertEqual(q.popBack(), 2)
        self.assertEqual(q.popFront(), -1)

    def test_pop_from_empty_returns_minus_one(self):
        q = FrontMiddleBackQueue()
        self.assertEqual(q.popFront(), -1)
        self.assertEqual(q.popMiddle(), -1)
        self.assertEqual(q.popBack(), -1)

    def test_single_element_all_pops(self):
        q = FrontMiddleBackQueue()
        q.pushFront(7)
        self.assertEqual(q.popMiddle(), 7)
        q.pushBack(8)
        self.assertEqual(q.popFront(), 8)
        q.pushMiddle(9)
        self.assertEqual(q.popBack(), 9)

    def test_push_middle_on_empty(self):
        q = FrontMiddleBackQueue()
        q.pushMiddle(5)
        self.assertEqual(q.popFront(), 5)

    def test_push_middle_frontmost_rule_odd_length(self):
        # State [1,2,3,4,5]; pushMiddle(6) -> [1,2,6,3,4,5]
        q = FrontMiddleBackQueue()
        for v in (1, 2, 3, 4, 5):
            q.pushBack(v)
        q.pushMiddle(6)
        out = []
        while True:
            x = q.popFront()
            if x == -1:
                break
            out.append(x)
        self.assertEqual(out, [1, 2, 6, 3, 4, 5])

    def test_pop_middle_frontmost_rule_even_length(self):
        # State [1,2,3,4,5,6]; popMiddle() -> 3, leaves [1,2,4,5,6]
        q = FrontMiddleBackQueue()
        for v in (1, 2, 3, 4, 5, 6):
            q.pushBack(v)
        self.assertEqual(q.popMiddle(), 3)
        out = []
        while True:
            x = q.popFront()
            if x == -1:
                break
            out.append(x)
        self.assertEqual(out, [1, 2, 4, 5, 6])

    def test_push_middle_on_two_element(self):
        # State [1,2]; pushMiddle(9) -> [1,9,2] (frontmost middle slot is index 1)
        q = FrontMiddleBackQueue()
        q.pushBack(1)
        q.pushBack(2)
        q.pushMiddle(9)
        self.assertEqual(q.popFront(), 1)
        self.assertEqual(q.popFront(), 9)
        self.assertEqual(q.popFront(), 2)

    def test_pop_middle_on_two_element_returns_front(self):
        # State [1,2]; popMiddle() -> 1 (frontmost of two middles)
        q = FrontMiddleBackQueue()
        q.pushBack(1)
        q.pushBack(2)
        self.assertEqual(q.popMiddle(), 1)
        self.assertEqual(q.popFront(), 2)

    def test_only_front_pushes_then_pop_back(self):
        q = FrontMiddleBackQueue()
        for v in (1, 2, 3, 4):
            q.pushFront(v)  # state becomes [4,3,2,1]
        self.assertEqual(q.popBack(), 1)
        self.assertEqual(q.popBack(), 2)
        self.assertEqual(q.popFront(), 4)
        self.assertEqual(q.popFront(), 3)
        self.assertEqual(q.popFront(), -1)

    def test_mixed_stress_against_reference_list(self):
        # Exercise rebalancing across many alternating ops by comparing to a list.
        q = FrontMiddleBackQueue()
        ref = []
        ops = [
            ("pf", 1), ("pb", 2), ("pm", 3), ("pf", 4), ("pb", 5),
            ("pm", 6), ("pf", 7), ("pb", 8), ("pm", 9), ("pm", 10),
        ]
        for kind, v in ops:
            if kind == "pf":
                q.pushFront(v)
                ref.insert(0, v)
            elif kind == "pb":
                q.pushBack(v)
                ref.append(v)
            else:
                q.pushMiddle(v)
                ref.insert(len(ref) // 2, v)
        # Drain via popFront and compare.
        drained = []
        while True:
            x = q.popFront()
            if x == -1:
                break
            drained.append(x)
        self.assertEqual(drained, ref)

    def test_large_value_allowed(self):
        q = FrontMiddleBackQueue()
        q.pushBack(10**9)
        self.assertEqual(q.popBack(), 10**9)


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  — peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
Two-deque split. Keep the queue logically as `front + back`, where the
boundary always sits at the conceptual middle:

    front = [ ... left half ... ]    back = [ ... right half ... ]

Invariant after every operation:
    len(front) <= len(back) <= len(front) + 1

That single invariant pins down every "middle" rule the problem cares about:
  - When the total is EVEN, the two halves are equal in size, and the
    frontmost-middle index sits at the back of `front` -> front.pop().
  - When the total is ODD, `back` has one extra and the middle sits at the
    front of `back` -> back.popleft().

Rebalance helper (call after every mutation):
  - If len(back) > len(front) + 1: front.append(back.popleft())
  - If len(front) > len(back):     back.appendleft(front.pop())

That's it. Every operation is O(1) amortized: the two-deque trick is
exactly the queue analog of "two heaps for median".

Operations
----------
- pushFront(v):  front.appendleft(v); rebalance()
- pushBack(v):   back.append(v); rebalance()
- pushMiddle(v): front.append(v); rebalance()   # rebalance pushes the
                                                # extra back into `back`
                                                # when the queue is even-length,
                                                # which is exactly the
                                                # frontmost-middle slot.
- popFront():    if empty -> -1
                 if front: return front.popleft()
                 else:     return back.popleft()   # whole queue lives in back
                 then rebalance()
- popMiddle():   if empty -> -1
                 if len(front) == len(back): return front.pop()
                 else:                       return back.popleft()
- popBack():     if not back: return -1            # back empty => total empty
                 v = back.pop(); rebalance(); return v

Complexity
----------
- Time:  O(1) amortized per operation. (No shifting, no scanning.)
- Space: O(n) for the elements stored.

Python solution
---------------
from collections import deque

class FrontMiddleBackQueue:
    def __init__(self):
        self.front = deque()
        self.back = deque()

    def _rebalance(self):
        # Enforce len(front) <= len(back) <= len(front) + 1
        if len(self.back) > len(self.front) + 1:
            self.front.append(self.back.popleft())
        elif len(self.front) > len(self.back):
            self.back.appendleft(self.front.pop())

    def pushFront(self, val):
        self.front.appendleft(val)
        self._rebalance()

    def pushMiddle(self, val):
        # Append at the boundary; rebalance shoves it into `back`
        # exactly when the queue is even-length, which is the
        # frontmost-middle slot.
        self.front.append(val)
        self._rebalance()

    def pushBack(self, val):
        self.back.append(val)
        self._rebalance()

    def popFront(self):
        if not self.front and not self.back:
            return -1
        v = self.front.popleft() if self.front else self.back.popleft()
        self._rebalance()
        return v

    def popMiddle(self):
        if not self.front and not self.back:
            return -1
        if len(self.front) == len(self.back):
            return self.front.pop()    # even total -> frontmost middle
        return self.back.popleft()     # odd total  -> single middle in `back`

    def popBack(self):
        if not self.back:
            return -1
        v = self.back.pop()
        self._rebalance()
        return v

Interview tips
--------------
- State the invariant first: "two deques, len(front) <= len(back) <= len(front)+1."
  Everything else falls out of it. Don't try to derive the special cases
  problem-by-problem on the whiteboard — derive them from the invariant.
- Trace the LeetCode example out loud as a sanity check (pushFront 1,
  pushBack 2, pushMiddle 3, pushMiddle 4) and show the (front, back) split
  at each step: ([],[1]) -> ([1],[2]) -> ([1],[3,2]) -> ([1,4],[3,2])... wait,
  that violates the invariant -> rebalance to ([1],[4,3,2]). Catching that
  rebalance in real time is the whole point of the design.
- The boundary trick is the same idea as "two heaps for running median"
  and "stack of stacks for capacity-bounded set" — call that out; it
  signals you recognize the pattern family.
- Don't reach for a single deque + index arithmetic — popMiddle becomes
  O(n) because deque has no O(1) random access. Two deques is the
  insight the question is testing.
- Watch the order on popFront when `front` is empty: the queue lives in
  `back`, so you popleft from `back`, not from `front`.
"""
