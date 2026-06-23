"""
LeetCode #142 - Linked List Cycle II  (Linked List - Medium)
URL: https://leetcode.com/problems/linked-list-cycle-ii/

Problem
-------
Given the head of a linked list, return the node where the cycle begins. If there
is no cycle, return null.

There is a cycle in a linked list if there is some node in the list that can be
reached again by continuously following the next pointer. Internally, pos is used
to denote the index of the node that tail's next pointer is connected to (0
-indexed). It is -1 if there is no cycle. Note that pos is NOT passed as a
parameter.

Do not modify the linked list.

Examples
--------
1) Input:  head = [3,2,0,-4], pos = 1
   Output: tail connects to node index 1
   Explanation: There is a cycle in the linked list, where tail connects to the
   second node (value 2).

2) Input:  head = [1,2], pos = 0
   Output: tail connects to node index 0

3) Input:  head = [1], pos = -1
   Output: no cycle

Constraints
-----------
- The number of the nodes in the list is in the range [0, 10^4].
- -10^5 <= Node.val <= 10^5
- pos is -1 or a valid index in the linked-list.

Follow-up
---------
Can you solve it using O(1) (i.e. constant) memory?

Run
---
    python 2026-06-23-linked-list-cycle-ii.py -v
"""

import unittest


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def detectCycle(self, head):
        raise NotImplementedError("Implement detectCycle")


def build_list_with_cycle(values, pos):
    """Build a linked list from values; connect tail.next to node at index pos.
    pos = -1 means no cycle. Returns (head, expected_cycle_node)."""
    if not values:
        return None, None
    nodes = [ListNode(v) for v in values]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    cycle_node = None
    if pos != -1:
        nodes[-1].next = nodes[pos]
        cycle_node = nodes[pos]
    return nodes[0], cycle_node


class TestDetectCycle(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1(self):
        head, expected = build_list_with_cycle([3, 2, 0, -4], 1)
        self.assertIs(self.sol.detectCycle(head), expected)

    def test_example_2(self):
        head, expected = build_list_with_cycle([1, 2], 0)
        self.assertIs(self.sol.detectCycle(head), expected)

    def test_single_node_no_cycle(self):
        head, expected = build_list_with_cycle([1], -1)
        self.assertIsNone(self.sol.detectCycle(head))

    def test_single_node_self_cycle(self):
        head, expected = build_list_with_cycle([1], 0)
        self.assertIs(self.sol.detectCycle(head), expected)

    def test_empty_list(self):
        self.assertIsNone(self.sol.detectCycle(None))

    def test_no_cycle_multiple(self):
        head, expected = build_list_with_cycle([1, 2, 3, 4, 5], -1)
        self.assertIsNone(self.sol.detectCycle(head))

    def test_cycle_at_head(self):
        head, expected = build_list_with_cycle([5, 6, 7, 8], 0)
        self.assertIs(self.sol.detectCycle(head), expected)

    def test_cycle_at_tail(self):
        head, expected = build_list_with_cycle([1, 2, 3], 2)
        self.assertIs(self.sol.detectCycle(head), expected)

    def test_does_not_modify_list(self):
        head, expected = build_list_with_cycle([3, 2, 0, -4], 1)
        # capture next pointers
        node = head
        snapshot = []
        for _ in range(4):
            snapshot.append(node.next)
            node = node.next
        self.sol.detectCycle(head)
        node = head
        for i in range(4):
            self.assertIs(node.next, snapshot[i])
            node = node.next


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  - peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
Floyd's tortoise-and-hare in two phases: first detect a cycle, then locate its
entry.

Phase 1 - detect:
  Move slow by 1 and fast by 2. If fast (or fast.next) reaches None, there is no
  cycle -> return None. Otherwise they eventually meet INSIDE the cycle.

Phase 2 - find entry:
  This is the classic distance argument. Let the distance from head to the cycle
  entry be a, and the meeting point be b nodes into the cycle. When slow and fast
  meet, one can show a is congruent to (cycle_length - b) modulo the cycle
  length. Concretely: reset one pointer to head, keep the other at the meeting
  point, then advance BOTH one step at a time. They meet exactly at the cycle
  entry.

Why phase 2 works: when slow has travelled a + b, fast has travelled 2(a + b),
and the difference 2(a+b) - (a+b) = a+b is a whole number of cycle loops. From
the meeting point, walking another a steps lands on the entry, which is also
exactly a steps from head. So two pointers a steps apart converge at the entry.

Complexity
----------
- Time:  O(n), each pointer travels at most a couple of passes.
- Space: O(1), only two pointers (satisfies the follow-up).

Python solution
---------------
class Solution:
    def detectCycle(self, head):
        slow = fast = head

        # Phase 1: detect a meeting point inside the cycle.
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                break
        else:
            return None            # loop ended without meeting -> no cycle

        # Phase 2: find the cycle entry.
        slow = head
        while slow is not fast:
            slow = slow.next
            fast = fast.next
        return slow

Interview tips
--------------
- Two phases: detect the meeting point, then walk one pointer from head and one
  from the meeting point at equal speed to find the entry.
- The `while...else` is handy: the else runs only if the loop exits normally
  (fast hit the end), meaning no cycle.
- Be careful with the fast-pointer guard: check both `fast` and `fast.next`
  before doing `fast.next.next` to avoid a None dereference.
- A hash set of visited nodes also finds the entry in O(n) time but O(n) space;
  mention it, then give Floyd's O(1)-space version for the follow-up.
- Compare nodes by identity (`is`), and do not modify the list (the problem
  forbids it).
"""
