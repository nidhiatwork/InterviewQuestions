"""LeetCode #622 — Design Circular Queue  (Queue · Medium)

URL: https://leetcode.com/problems/design-circular-queue/

Problem
-------
Design a fixed-capacity circular queue (ring buffer) with these methods:
  MyCircularQueue(k)  -> initialize capacity to k
  enQueue(value)      -> insert, return True/False
  deQueue()           -> remove from front, return True/False
  Front()             -> peek front or -1 if empty
  Rear()              -> peek rear  or -1 if empty
  isEmpty()           -> bool
  isFull()            -> bool

You MUST NOT use a built-in queue (deque, queue.Queue, etc.).

Constraints
-----------
  1 <= k <= 1000
  0 <= value <= 1000
  At most 3000 calls.

Run
---
  python 2026-05-07-design-circular-queue.py -v
"""

import unittest


class MyCircularQueue:
    def __init__(self, k):
        raise NotImplementedError("Implement __init__")

    def enQueue(self, value):
        raise NotImplementedError("Implement enQueue")

    def deQueue(self):
        raise NotImplementedError("Implement deQueue")

    def Front(self):
        raise NotImplementedError("Implement Front")

    def Rear(self):
        raise NotImplementedError("Implement Rear")

    def isEmpty(self):
        raise NotImplementedError("Implement isEmpty")

    def isFull(self):
        raise NotImplementedError("Implement isFull")


# ----------------------------- tests -----------------------------

class TestMyCircularQueue(unittest.TestCase):
    def test_leetcode_example_full_sequence(self):
        q = MyCircularQueue(3)
        self.assertTrue(q.enQueue(1))
        self.assertTrue(q.enQueue(2))
        self.assertTrue(q.enQueue(3))
        self.assertFalse(q.enQueue(4))
        self.assertEqual(q.Rear(), 3)
        self.assertTrue(q.isFull())
        self.assertTrue(q.deQueue())
        self.assertTrue(q.enQueue(4))
        self.assertEqual(q.Rear(), 4)

    def test_front_on_empty_returns_minus_one(self):
        self.assertEqual(MyCircularQueue(2).Front(), -1)

    def test_rear_on_empty_returns_minus_one(self):
        self.assertEqual(MyCircularQueue(2).Rear(), -1)

    def test_dequeue_on_empty_returns_false(self):
        self.assertFalse(MyCircularQueue(2).deQueue())

    def test_isempty_initially_true(self):
        q = MyCircularQueue(5)
        self.assertTrue(q.isEmpty())
        self.assertFalse(q.isFull())

    def test_capacity_one(self):
        q = MyCircularQueue(1)
        self.assertTrue(q.enQueue(7))
        self.assertTrue(q.isFull())
        self.assertFalse(q.enQueue(8))
        self.assertEqual(q.Front(), 7)
        self.assertEqual(q.Rear(), 7)
        self.assertTrue(q.deQueue())
        self.assertTrue(q.isEmpty())
        self.assertEqual(q.Front(), -1)

    def test_wraparound_after_dequeue(self):
        q = MyCircularQueue(3)
        q.enQueue(1); q.enQueue(2); q.enQueue(3)
        q.deQueue(); q.deQueue()
        self.assertTrue(q.enQueue(4))
        self.assertTrue(q.enQueue(5))
        self.assertEqual(q.Front(), 3)
        self.assertEqual(q.Rear(), 5)
        self.assertTrue(q.isFull())

    def test_full_drain_and_refill(self):
        q = MyCircularQueue(2)
        q.enQueue(10); q.enQueue(20)
        q.deQueue(); q.deQueue()
        self.assertTrue(q.isEmpty())
        self.assertTrue(q.enQueue(30))
        self.assertTrue(q.enQueue(40))
        self.assertEqual(q.Front(), 30)
        self.assertEqual(q.Rear(), 40)

    def test_alternating_enqueue_dequeue(self):
        q = MyCircularQueue(2)
        q.enQueue(1); q.deQueue()
        q.enQueue(2); q.deQueue()
        q.enQueue(3)
        self.assertEqual(q.Front(), 3)
        self.assertEqual(q.Rear(), 3)
        self.assertFalse(q.isEmpty())
        self.assertFalse(q.isFull())

    def test_zero_value_is_valid(self):
        q = MyCircularQueue(1)
        q.enQueue(0)
        self.assertEqual(q.Front(), 0)
        self.assertEqual(q.Rear(), 0)
        self.assertFalse(q.isEmpty())


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  — peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
Fixed-size array + head pointer + tail pointer + count field.

Why count? With only head and tail you can't distinguish empty from full
without wasting a slot or adding a flag. Tracking count makes the invariants
unambiguous and uses every position.

Operations
----------
- enQueue(v):  if full -> False; data[tail] = v; tail = (tail + 1) % cap; count++
- deQueue():   if empty -> False; head = (head + 1) % cap; count--
- Front():     -1 if empty else data[head]
- Rear():      -1 if empty else data[(tail - 1 + cap) % cap]
- isEmpty():   count == 0
- isFull():    count == cap

Complexity
----------
- Time:  O(1) per operation
- Space: O(k)

Python solution
---------------
class MyCircularQueue:
    def __init__(self, k):
        self._capacity = k
        self._data = [0] * k
        self._head = 0
        self._tail = 0
        self._count = 0

    def enQueue(self, value):
        if self.isFull():
            return False
        self._data[self._tail] = value
        self._tail = (self._tail + 1) % self._capacity
        self._count += 1
        return True

    def deQueue(self):
        if self.isEmpty():
            return False
        self._head = (self._head + 1) % self._capacity
        self._count -= 1
        return True

    def Front(self):
        return -1 if self.isEmpty() else self._data[self._head]

    def Rear(self):
        if self.isEmpty():
            return -1
        return self._data[(self._tail - 1 + self._capacity) % self._capacity]

    def isEmpty(self):
        return self._count == 0

    def isFull(self):
        return self._count == self._capacity

Interview tips
--------------
- State the empty-vs-full disambiguation up front ("I'll use a count field").
- Walk through Rear() carefully: (tail - 1 + capacity) % capacity. The
  `+ capacity` prevents a negative result when tail == 0.
- Don't bother zeroing on dequeue — the next enQueue overwrites the slot.
- 0 is a valid stored value, so any "is this slot live?" check must use
  count, not a sentinel scan of _data.
- Mention deque solves this in 5 lines but the problem forbids built-in queues.
"""
