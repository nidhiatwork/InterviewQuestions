# LeetCode #142 - Linked List Cycle II

**Data structure:** Linked List  
**Difficulty:** Medium  
**URL:** https://leetcode.com/problems/linked-list-cycle-ii/

## Problem

Given the head of a linked list, return the node where the cycle **begins**. If there is no cycle, return `null`.

`pos` denotes the index the tail's `next` connects to (0-indexed), or `-1` for no cycle; it is **not** passed as a parameter. Do not modify the list.

## Examples

```text
Input: head = [3,2,0,-4], pos = 1
Output: node at index 1 (value 2)
```

```text
Input: head = [1,2], pos = 0
Output: node at index 0
```

```text
Input: head = [1], pos = -1
Output: null (no cycle)
```

## Constraints

- The number of nodes is in the range `[0, 10^4]`.
- `-10^5 <= Node.val <= 10^5`
- `pos` is `-1` or a valid index.

**Follow-up:** Solve using `O(1)` memory.

## Approach

Floyd's tortoise-and-hare in two phases: first detect a cycle, then locate its entry.

**Phase 1 — detect:** move `slow` by 1 and `fast` by 2. If `fast` (or `fast.next`) reaches `None`, there's no cycle → return `None`. Otherwise they meet **inside** the cycle.

**Phase 2 — find entry:** reset one pointer to `head`, keep the other at the meeting point, then advance **both** one step at a time. They meet exactly at the cycle entry.

Why phase 2 works: let `a` be the distance from head to the entry and the meeting point be `b` nodes into the cycle. When they meet, `slow` travelled `a + b` and `fast` travelled `2(a + b)`, so the difference `a + b` is a whole number of loops. Walking another `a` steps from the meeting point lands on the entry — which is also `a` steps from head. Two pointers `a` apart converge at the entry.

**Complexity**

- Time: `O(n)`
- Space: `O(1)` — two pointers (satisfies the follow-up)

## Python solution

```python
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
```

## unittest test cases

```python
import unittest


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build_list_with_cycle(values, pos):
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

    def test_no_cycle(self):
        head, _ = build_list_with_cycle([1, 2, 3, 4, 5], -1)
        self.assertIsNone(self.sol.detectCycle(head))

    def test_empty_list(self):
        self.assertIsNone(self.sol.detectCycle(None))

    def test_self_cycle(self):
        head, expected = build_list_with_cycle([1], 0)
        self.assertIs(self.sol.detectCycle(head), expected)

    def test_cycle_at_head(self):
        head, expected = build_list_with_cycle([5, 6, 7, 8], 0)
        self.assertIs(self.sol.detectCycle(head), expected)
```

## Interview tips

- Two phases: detect the meeting point, then walk one pointer from head and one from the meeting point at equal speed to find the entry.
- The `while...else` is handy: the `else` runs only if the loop exits normally (fast hit the end), meaning no cycle.
- Guard the fast pointer: check both `fast` and `fast.next` before `fast.next.next` to avoid a `None` dereference.
- A hash set of visited nodes also finds the entry in `O(n)` time but `O(n)` space — mention it, then give Floyd's `O(1)`-space version.
- Compare nodes by identity (`is`) and do not modify the list (the problem forbids it).
