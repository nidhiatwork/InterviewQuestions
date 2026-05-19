"""LeetCode #2 — Add Two Numbers  (Linked List · Medium)

URL: https://leetcode.com/problems/add-two-numbers/

Problem
-------
You are given two non-empty linked lists representing two non-negative integers.
The digits are stored in REVERSE order, and each node contains a single digit.
Add the two numbers and return the sum as a linked list.

Examples
--------
  l1 = [2,4,3], l2 = [5,6,4]                  -> [7,0,8]      (342 + 465 = 807)
  l1 = [0], l2 = [0]                          -> [0]
  l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]        -> [8,9,9,9,0,0,0,1]

Constraints
-----------
  Each list has 1 to 100 nodes; 0 <= Node.val <= 9; no leading zeros.

Run
---
  python 2026-05-05-add-two-numbers.py -v
"""

import unittest


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def addTwoNumbers(self, l1, l2):
        raise NotImplementedError("Implement addTwoNumbers")


# ----------------------------- helpers -----------------------------

def list_to_linked(values):
    dummy = ListNode()
    tail = dummy
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def linked_to_list(head):
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
    return out


# ----------------------------- tests -----------------------------

class TestAddTwoNumbers(unittest.TestCase):
    def setUp(self):
        self.s = Solution()

    def test_example_1(self):
        l1 = list_to_linked([2, 4, 3])
        l2 = list_to_linked([5, 6, 4])
        self.assertEqual(linked_to_list(self.s.addTwoNumbers(l1, l2)), [7, 0, 8])

    def test_zero_plus_zero(self):
        l1 = list_to_linked([0])
        l2 = list_to_linked([0])
        self.assertEqual(linked_to_list(self.s.addTwoNumbers(l1, l2)), [0])

    def test_carry_creates_new_node(self):
        l1 = list_to_linked([5])
        l2 = list_to_linked([5])
        self.assertEqual(linked_to_list(self.s.addTwoNumbers(l1, l2)), [0, 1])

    def test_different_lengths(self):
        l1 = list_to_linked([9, 9, 9, 9, 9, 9, 9])
        l2 = list_to_linked([9, 9, 9, 9])
        self.assertEqual(
            linked_to_list(self.s.addTwoNumbers(l1, l2)),
            [8, 9, 9, 9, 0, 0, 0, 1],
        )

    def test_long_list_no_final_carry(self):
        l1 = list_to_linked([0, 0, 1])
        l2 = list_to_linked([1])
        self.assertEqual(linked_to_list(self.s.addTwoNumbers(l1, l2)), [1, 0, 1])

    def test_one_short_other_long(self):
        l1 = list_to_linked([1, 2, 3])
        l2 = list_to_linked([0])
        self.assertEqual(linked_to_list(self.s.addTwoNumbers(l1, l2)), [1, 2, 3])

    def test_input_not_mutated(self):
        l1_values = [2, 4, 3]
        l2_values = [5, 6, 4]
        l1 = list_to_linked(l1_values)
        l2 = list_to_linked(l2_values)
        self.s.addTwoNumbers(l1, l2)
        self.assertEqual(linked_to_list(l1), l1_values)
        self.assertEqual(linked_to_list(l2), l2_values)


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  — peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
Dummy-node pattern + single pass with carry. Walk both lists simultaneously.
At each position sum the two current digits plus an incoming carry; write
sum % 10 to a new node and propagate sum // 10 as the next carry. The dummy
head eliminates the "is this the first node?" branch.

Three things candidates miss:
  1. Lists may have different lengths -> treat missing as 0.
  2. A final carry can produce a new node (e.g. 5 + 5 = 10).
  3. Don't mutate the input lists.

Complexity
----------
- Time:  O(max(m, n))
- Space: O(max(m, n))  (output list)

Python solution
---------------
class Solution:
    def addTwoNumbers(self, l1, l2):
        dummy = ListNode()
        tail = dummy
        carry = 0
        while l1 or l2 or carry:
            v1 = l1.val if l1 else 0
            v2 = l2.val if l2 else 0
            total = v1 + v2 + carry
            carry, digit = divmod(total, 10)
            tail.next = ListNode(digit)
            tail = tail.next
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None
        return dummy.next

Interview tips
--------------
- Dummy-node pattern is the headline answer — interviewers look for it.
- `while l1 or l2 or carry` is the elegant single-line form; many candidates
  write three separate loops.
- `divmod(total, 10)` is Pythonic for (carry, digit).
- DON'T convert to int first, sum, then convert back — fails the 100-digit
  constraint in languages without bignum (Java, C++). Always digit-by-digit.
- Follow-up: "What if digits were in forward order?" Reverse both lists, run
  this algorithm, reverse the output. Or use two stacks.
"""
