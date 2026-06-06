"""
LeetCode #92 - Reverse Linked List II  (Linked List · Medium)
URL: https://leetcode.com/problems/reverse-linked-list-ii/

Problem
-------
Given the head of a singly linked list and two integers left and right where
left <= right, reverse the nodes of the list from position left to position
right, and return the reversed list.

Positions are 1-indexed.

Examples
--------
1) Input:  head = [1,2,3,4,5], left = 2, right = 4
   Output: [1,4,3,2,5]

2) Input:  head = [5], left = 1, right = 1
   Output: [5]

3) Input:  head = [1,2,3], left = 1, right = 2
   Output: [2,1,3]

Constraints
-----------
- The number of nodes in the list is n.
- 1 <= n <= 500
- -500 <= Node.val <= 500
- 1 <= left <= right <= n

Run
---
    python 2026-06-06-reverse-linked-list-ii.py -v
"""

import unittest


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def reverseBetween(self, head, left, right):
        raise NotImplementedError("Implement reverseBetween")


def list_to_linked(values):
    dummy = ListNode()
    cur = dummy
    for value in values:
        cur.next = ListNode(value)
        cur = cur.next
    return dummy.next


def linked_to_list(head):
    values = []
    while head:
        values.append(head.val)
        head = head.next
    return values


class TestReverseBetween(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def assertReverse(self, values, left, right, expected):
        head = list_to_linked(values)
        result = self.sol.reverseBetween(head, left, right)
        self.assertEqual(linked_to_list(result), expected)

    def test_example_middle_segment(self):
        self.assertReverse([1, 2, 3, 4, 5], 2, 4, [1, 4, 3, 2, 5])

    def test_single_node(self):
        self.assertReverse([5], 1, 1, [5])

    def test_reverse_from_head(self):
        self.assertReverse([1, 2, 3], 1, 2, [2, 1, 3])

    def test_reverse_entire_list(self):
        self.assertReverse([1, 2, 3, 4], 1, 4, [4, 3, 2, 1])

    def test_left_equals_right_no_change(self):
        self.assertReverse([1, 2, 3, 4], 3, 3, [1, 2, 3, 4])

    def test_reverse_tail_segment(self):
        self.assertReverse([10, 20, 30, 40, 50], 3, 5, [10, 20, 50, 40, 30])

    def test_two_nodes_reverse(self):
        self.assertReverse([7, 8], 1, 2, [8, 7])

    def test_negative_values(self):
        self.assertReverse([-1, -2, -3, -4], 2, 3, [-1, -3, -2, -4])


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  - peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
Use a dummy node before the head so reversing from position 1 is handled the
same way as reversing a middle segment.

1. Move `prev` to the node immediately before position `left`.
2. Let `cur = prev.next`; this is the first node in the segment and will become
   the tail of the reversed segment.
3. Repeatedly take the node after `cur` and move it to the front of the segment.
4. After `right - left` moves, the requested window is reversed in place.

For [1,2,3,4,5], left=2, right=4:
- prev points to 1, cur points to 2
- move 3 after prev: [1,3,2,4,5]
- move 4 after prev: [1,4,3,2,5]

Complexity
----------
- Time:  O(n), because each pointer is advanced or rewired a constant number of times.
- Space: O(1), because the reversal is done in place.

Python solution
---------------
class Solution:
    def reverseBetween(self, head, left, right):
        if left == right:
            return head

        dummy = ListNode(0, head)
        prev = dummy

        for _ in range(left - 1):
            prev = prev.next

        cur = prev.next
        for _ in range(right - left):
            move = cur.next
            cur.next = move.next
            move.next = prev.next
            prev.next = move

        return dummy.next

Interview tips
--------------
- Draw the three important pointers: `prev`, `cur`, and `move`.
- The dummy node removes special handling when left == 1.
- Keep `cur` fixed during the inner loop; nodes after it are moved to the front.
- Be careful with 1-indexing. Move `prev` exactly `left - 1` times from dummy.
- Mention that no node values are swapped; only links are rewired.
"""
