"""
LeetCode #380 - Insert Delete GetRandom O(1)  (Hash Table · Medium)
URL: https://leetcode.com/problems/insert-delete-getrandom-o1/

Problem
-------
Implement the RandomizedSet class:

- RandomizedSet() initializes the object.
- bool insert(int val) inserts val into the set if not present. Returns true if
  val was not present, false otherwise.
- bool remove(int val) removes val from the set if present. Returns true if val
  was present, false otherwise.
- int getRandom() returns a random element from the current set of elements.

Each function must work in average O(1) time.

Examples
--------
1) Input:
   ["RandomizedSet", "insert", "remove", "insert", "getRandom", "remove", "insert", "getRandom"]
   [[], [1], [2], [2], [], [1], [2], []]
   Output: [null, true, false, true, 2, true, false, 2]

2) Input:
   ["RandomizedSet", "insert", "insert", "remove", "insert", "getRandom"]
   [[], [10], [10], [10], [20], []]
   Output: [null, true, false, true, true, 20]

3) Input:
   ["RandomizedSet", "insert", "insert", "remove", "getRandom"]
   [[], [-1], [0], [-1], []]
   Output: [null, true, true, true, 0]

Constraints
-----------
- -2^31 <= val <= 2^31 - 1
- At most 2 * 10^5 calls will be made to insert, remove, and getRandom.
- There will be at least one element in the data structure when getRandom is called.

Run
---
    python 2026-06-04-insert-delete-getrandom-o1.py -v
"""

import random
import unittest


class RandomizedSet:
    def __init__(self):
        raise NotImplementedError("Implement __init__")

    def insert(self, val):
        raise NotImplementedError("Implement insert")

    def remove(self, val):
        raise NotImplementedError("Implement remove")

    def getRandom(self):
        raise NotImplementedError("Implement getRandom")


class TestRandomizedSet(unittest.TestCase):
    def test_example_flow(self):
        rs = RandomizedSet()
        self.assertTrue(rs.insert(1))
        self.assertFalse(rs.remove(2))
        self.assertTrue(rs.insert(2))
        self.assertIn(rs.getRandom(), {1, 2})
        self.assertTrue(rs.remove(1))
        self.assertFalse(rs.insert(2))
        self.assertEqual(rs.getRandom(), 2)

    def test_duplicate_insert_returns_false(self):
        rs = RandomizedSet()
        self.assertTrue(rs.insert(10))
        self.assertFalse(rs.insert(10))
        self.assertTrue(rs.remove(10))
        self.assertTrue(rs.insert(10))

    def test_remove_missing_returns_false(self):
        rs = RandomizedSet()
        self.assertFalse(rs.remove(99))
        self.assertTrue(rs.insert(99))
        self.assertFalse(rs.remove(100))
        self.assertTrue(rs.remove(99))

    def test_get_random_returns_existing_value(self):
        rs = RandomizedSet()
        values = {4, 8, 15, 16, 23, 42}
        for value in values:
            self.assertTrue(rs.insert(value))
        for _ in range(50):
            self.assertIn(rs.getRandom(), values)

    def test_remove_last_element_then_insert_new_one(self):
        rs = RandomizedSet()
        self.assertTrue(rs.insert(-1))
        self.assertTrue(rs.remove(-1))
        self.assertTrue(rs.insert(0))
        self.assertEqual(rs.getRandom(), 0)

    def test_remove_middle_keeps_structure_usable(self):
        rs = RandomizedSet()
        for value in [1, 2, 3, 4]:
            self.assertTrue(rs.insert(value))
        self.assertTrue(rs.remove(2))
        remaining = {1, 3, 4}
        for _ in range(50):
            self.assertIn(rs.getRandom(), remaining)
        self.assertFalse(rs.remove(2))
        self.assertTrue(rs.insert(2))

    def test_many_operations(self):
        rs = RandomizedSet()
        for value in range(100):
            self.assertTrue(rs.insert(value))
        for value in range(0, 100, 2):
            self.assertTrue(rs.remove(value))
        odds = set(range(1, 100, 2))
        for _ in range(50):
            self.assertIn(rs.getRandom(), odds)


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  — peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
The core challenge is making remove O(1). A hash set alone can insert and check
membership quickly, but it cannot return a random element by index. A list can
return a random element quickly, but removing from the middle is expensive.

Use both:

1. `values` stores the current elements in a compact list.
2. `index` maps each value to its current position in `values`.
3. insert appends to `values` and records the index.
4. remove swaps the target value with the last list element, pops the last slot,
   and updates the swapped value's index.
5. getRandom picks a random list index.

The swap-with-last trick is the key. It avoids shifting list elements after a
middle removal, so every operation stays average O(1).

Complexity
----------
- Time:  O(1) average for insert, remove, and getRandom.
- Space: O(n) for the list plus the value-to-index hash table.

Python solution
---------------
class RandomizedSet:
    def __init__(self):
        self.values = []
        self.index = {}

    def insert(self, val):
        if val in self.index:
            return False
        self.index[val] = len(self.values)
        self.values.append(val)
        return True

    def remove(self, val):
        if val not in self.index:
            return False

        remove_at = self.index[val]
        last_val = self.values[-1]

        self.values[remove_at] = last_val
        self.index[last_val] = remove_at

        self.values.pop()
        del self.index[val]
        return True

    def getRandom(self):
        return random.choice(self.values)

Interview tips
--------------
- State why a plain set is insufficient: it has no O(1) random-by-index access.
- State why a plain list is insufficient: middle removal shifts elements.
- The swap-with-last operation is the main insight; walk through it slowly.
- Be careful when removing the last element itself. The same swap code still
  works because `last_val == val`, then the index entry is deleted.
- In Python, `random.choice(self.values)` is the cleanest getRandom.
"""
