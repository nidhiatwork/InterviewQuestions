# LeetCode #380 — Insert Delete GetRandom O(1)

**Data structure:** Hash Table  
**Difficulty:** Medium  
**URL:** https://leetcode.com/problems/insert-delete-getrandom-o1/

## Problem

Implement the `RandomizedSet` class:

- `RandomizedSet()` initializes the object.
- `insert(val)` inserts `val` if it is not already present and returns whether the insert happened.
- `remove(val)` removes `val` if it is present and returns whether the remove happened.
- `getRandom()` returns a random element from the current set.

Each operation must run in average `O(1)` time.

## Examples

```text
Input:
["RandomizedSet", "insert", "remove", "insert", "getRandom", "remove", "insert", "getRandom"]
[[], [1], [2], [2], [], [1], [2], []]

Output:
[null, true, false, true, 2, true, false, 2]
```

```text
Input:
["RandomizedSet", "insert", "insert", "remove", "insert", "getRandom"]
[[], [10], [10], [10], [20], []]

Output:
[null, true, false, true, true, 20]
```

## Constraints

- `-2^31 <= val <= 2^31 - 1`
- At most `2 * 10^5` calls will be made to `insert`, `remove`, and `getRandom`.
- `getRandom` is called only when the set contains at least one element.

## Approach

Combine a list with a hash table:

1. Keep all current values in a compact list, so `getRandom` can pick a random index.
2. Keep a dictionary from value to list index, so membership checks and index lookup are `O(1)`.
3. To remove a value from the middle, swap it with the last value, pop the last slot, and update the swapped value's index.

The swap-with-last trick avoids shifting list elements, which is what keeps removal average `O(1)`.

**Complexity**

- Time: `O(1)` average for `insert`, `remove`, and `getRandom`
- Space: `O(n)`

## Python solution

```python
import random


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
```

## unittest test cases

```python
import unittest


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

    def test_remove_middle_keeps_structure_usable(self):
        rs = RandomizedSet()
        for value in [1, 2, 3, 4]:
            self.assertTrue(rs.insert(value))
        self.assertTrue(rs.remove(2))
        for _ in range(50):
            self.assertIn(rs.getRandom(), {1, 3, 4})
        self.assertFalse(rs.remove(2))
        self.assertTrue(rs.insert(2))
```

## Interview tips

- Explain why neither a plain set nor a plain list is enough by itself.
- The key phrase is "swap with the last element before popping."
- Be explicit that the dictionary stores indexes, not counts.
- Call out the last-element removal edge case; the same code still works.
- In Python, `random.choice(self.values)` is the simplest random access.
