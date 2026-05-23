"""LeetCode #19 — Remove Nth Node From End of List  (Linked List · Medium)

URL: https://leetcode.com/problems/remove-nth-node-from-end-of-list/

Problem
-------
Given the head of a linked list, remove the n-th node from the end of the
list and return its head. n is guaranteed to be valid (1 <= n <= length).
Try to do it in one pass.

Examples
--------
  head = [1,2,3,4,5], n = 2  ->  [1,2,3,5]      (remove the 4, which is 2nd from end)
  head = [1],         n = 1  ->  []             (remove the only node)
  head = [1,2],       n = 1  ->  [1]            (remove the tail)
  head = [1,2],       n = 2  ->  [2]            (remove the head)

Constraints
-----------
  1 <= length <= 30
  0 <= Node.val <= 100
  1 <= n <= length

Run
---
  python 2026-05-23-remove-nth-node-from-end-of-list.py -v
"""

import unittest


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def removeNthFromEnd(self, head, n):
        raise NotImplementedError("Implement removeNthFromEnd")


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

class TestRemoveNthFromEnd(unittest.TestCase):
    def setUp(self):
        self.s = Solution()

    def test_example_1(self):
        head = list_to_linked([1, 2, 3, 4, 5])
        result = self.s.removeNthFromEnd(head, 2)
        self.assertEqual(linked_to_list(result), [1, 2, 3, 5])

    def test_single_node_removed(self):
        head = list_to_linked([1])
        result = self.s.removeNthFromEnd(head, 1)
        self.assertEqual(linked_to_list(result), [])

    def test_remove_tail_of_two(self):
        head = list_to_linked([1, 2])
        result = self.s.removeNthFromEnd(head, 1)
        self.assertEqual(linked_to_list(result), [1])

    def test_remove_head_of_two(self):
        head = list_to_linked([1, 2])
        result = self.s.removeNthFromEnd(head, 2)
        self.assertEqual(linked_to_list(result), [2])

    def test_remove_head_of_many(self):
        head = list_to_linked([1, 2, 3, 4, 5])
        result = self.s.removeNthFromEnd(head, 5)
        self.assertEqual(linked_to_list(result), [2, 3, 4, 5])

    def test_remove_tail_of_many(self):
        head = list_to_linked([1, 2, 3, 4, 5])
        result = self.s.removeNthFromEnd(head, 1)
        self.assertEqual(linked_to_list(result), [1, 2, 3, 4])

    def test_remove_middle(self):
        head = list_to_linked([10, 20, 30, 40, 50, 60, 70])
        result = self.s.removeNthFromEnd(head, 4)
        self.assertEqual(linked_to_list(result), [10, 20, 30, 50, 60, 70])

    def test_values_with_duplicates(self):
        head = list_to_linked([5, 5, 5, 5])
        result = self.s.removeNthFromEnd(head, 2)
        self.assertEqual(linked_to_list(result), [5, 5, 5])

    def test_values_with_zeros(self):
        head = list_to_linked([0, 0, 0])
        result = self.s.removeNthFromEnd(head, 3)
        self.assertEqual(linked_to_list(result), [0, 0])

    def test_max_size_remove_first(self):
        values = list(range(30))
        head = list_to_linked(values)
        result = self.s.removeNthFromEnd(head, 30)
        self.assertEqual(linked_to_list(result), values[1:])

    def test_max_size_remove_last(self):
        values = list(range(30))
        head = list_to_linked(values)
        result = self.s.removeNthFromEnd(head, 1)
        self.assertEqual(linked_to_list(result), values[:-1])

    def test_max_size_remove_middle(self):
        values = list(range(1, 31))
        head = list_to_linked(values)
        result = self.s.removeNthFromEnd(head, 15)
        expected = values[:15] + values[16:]
        self.assertEqual(linked_to_list(result), expected)


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  — peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
Two pointers with a gap of n + a dummy node. Classic streaming pattern — no
recursion, no length counting, single pass.

  1. Create dummy -> head.  Anchor `slow` and `fast` at dummy.
  2. Advance `fast` exactly n+1 steps.  Now the gap between fast and slow is n+1.
  3. Walk both pointers one step at a time until `fast` is None.  When that
     happens, slow sits at the node *just before* the one to delete.
  4. Splice: slow.next = slow.next.next.
  5. Return dummy.next  (NOT head — head itself might have been the deletion).

The dummy node is the key trick. Without it you need a special "remove the
head" branch.  With it, removing the head is just "slow lands on dummy and
re-points dummy.next".

Why n+1 steps and not n?
  After n+1 advances, slow.next is the n-th-from-end node. That's exactly
  the node we want to bypass. If you advance n steps, slow IS the target
  node and you have no handle to its predecessor.

Complexity
----------
- Time:  O(L)  — single pass over a list of length L
- Space: O(1)  — two pointers + dummy

Python solution
---------------
class Solution:
    def removeNthFromEnd(self, head, n):
        dummy = ListNode(0, head)
        slow = dummy
        fast = dummy
        for _ in range(n + 1):
            fast = fast.next
        while fast is not None:
            slow = slow.next
            fast = fast.next
        slow.next = slow.next.next
        return dummy.next

Interview tips
--------------
- Lead with the dummy-node + two-pointer pattern — that's the headline.
  Interviewers actively listen for "I'll use a dummy so deleting the head
  isn't a special case."
- Watch the off-by-one: it's n+1 advances, not n. Walk through n=2 on
  [1,2,3,4,5] verbally — fast moves to index 3 (value 4), then both walk
  until fast is None; slow lands on index 2 (value 3), which is the node
  before the one we delete.
- Two-pass solution (count length L, then remove (L-n)+1'th node) is fine
  but interviewers will ask "can you do it in one pass?" Be ready with
  the two-pointer answer immediately.
- Recursion works too (return depth from each call), but it's O(L) stack
  and harder to explain on a whiteboard. Don't lead with it.
- Edge case to call out aloud: when n == length, the head itself is
  removed. The dummy makes this just work; without it you'd need an
  `if slow == dummy: return head.next` branch.
- Don't forget to *return* dummy.next, not head.  If you return head and
  the head was deleted, you return a dangling node.
"""
