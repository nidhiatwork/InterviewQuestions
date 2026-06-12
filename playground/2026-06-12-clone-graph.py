"""
LeetCode #133 - Clone Graph  (Graph - Medium)
URL: https://leetcode.com/problems/clone-graph/

Problem
-------
Given a reference of a node in a connected undirected graph, return a deep copy
(clone) of the graph.

Each node in the graph contains a value (int) and a list of its neighbors.

    class Node:
        val: int
        neighbors: List[Node]

Test case format
----------------
For simplicity, each node's value is the same as the node's index (1-indexed).
The graph is represented in the tests using an adjacency list. The given node is
always the first node with val = 1.

You must return the copy of the given node as a reference to the cloned graph.

Examples
--------
1) Input:  adjList = [[2,4],[1,3],[2,4],[1,3]]
   Output: [[2,4],[1,3],[2,4],[1,3]]
   Explanation: There are 4 nodes in the graph. Node 1's neighbors are 2 and 4,
   node 2's neighbors are 1 and 3, etc.

2) Input:  adjList = [[]]
   Output: [[]]
   Explanation: A single node with no neighbors.

3) Input:  adjList = []
   Output: []
   Explanation: The graph is empty (given node is null).

Constraints
-----------
- The number of nodes in the graph is in the range [0, 100].
- 1 <= Node.val <= 100
- Node.val is unique for each node.
- There are no repeated edges and no self-loops in the graph.
- The graph is connected and all nodes can be visited starting from the given
  node.

Run
---
    python 2026-06-12-clone-graph.py -v
"""

import unittest


class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


class Solution:
    def cloneGraph(self, node):
        raise NotImplementedError("Implement cloneGraph")


def build_graph(adj_list):
    """Build a graph from a 1-indexed adjacency list. Returns node with val=1."""
    if not adj_list:
        return None
    nodes = {i + 1: Node(i + 1) for i in range(len(adj_list))}
    for i, neighbors in enumerate(adj_list):
        nodes[i + 1].neighbors = [nodes[n] for n in neighbors]
    return nodes[1]


def to_adj_list(node):
    """Serialize a graph back to a 1-indexed adjacency list via BFS."""
    if node is None:
        return []
    from collections import deque

    seen = {}
    queue = deque([node])
    seen[node.val] = node
    while queue:
        cur = queue.popleft()
        for nb in cur.neighbors:
            if nb.val not in seen:
                seen[nb.val] = nb
                queue.append(nb)
    result = []
    for val in sorted(seen):
        result.append(sorted(nb.val for nb in seen[val].neighbors))
    return result


def collect_ids(node):
    """Return the set of python object ids reachable from node (for deep-copy checks)."""
    if node is None:
        return set()
    from collections import deque

    ids = set()
    queue = deque([node])
    ids.add(id(node))
    while queue:
        cur = queue.popleft()
        for nb in cur.neighbors:
            if id(nb) not in ids:
                ids.add(id(nb))
                queue.append(nb)
    return ids


class TestCloneGraph(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_four_node_graph(self):
        original = build_graph([[2, 4], [1, 3], [2, 4], [1, 3]])
        clone = self.sol.cloneGraph(original)
        self.assertEqual(to_adj_list(clone), [[2, 4], [1, 3], [2, 4], [1, 3]])

    def test_single_node_no_neighbors(self):
        original = build_graph([[]])
        clone = self.sol.cloneGraph(original)
        self.assertEqual(to_adj_list(clone), [[]])
        self.assertEqual(clone.val, 1)

    def test_empty_graph(self):
        clone = self.sol.cloneGraph(None)
        self.assertIsNone(clone)

    def test_two_node_graph(self):
        original = build_graph([[2], [1]])
        clone = self.sol.cloneGraph(original)
        self.assertEqual(to_adj_list(clone), [[2], [1]])

    def test_is_deep_copy(self):
        original = build_graph([[2, 4], [1, 3], [2, 4], [1, 3]])
        clone = self.sol.cloneGraph(original)
        orig_ids = collect_ids(original)
        clone_ids = collect_ids(clone)
        # No node object should be shared between original and clone.
        self.assertEqual(orig_ids & clone_ids, set())

    def test_clone_values_match(self):
        original = build_graph([[2, 4], [1, 3], [2, 4], [1, 3]])
        clone = self.sol.cloneGraph(original)
        self.assertEqual(clone.val, 1)
        self.assertEqual(sorted(nb.val for nb in clone.neighbors), [2, 4])

    def test_triangle_graph(self):
        original = build_graph([[2, 3], [1, 3], [1, 2]])
        clone = self.sol.cloneGraph(original)
        self.assertEqual(to_adj_list(clone), [[2, 3], [1, 3], [1, 2]])


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  - peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
Traverse the graph while keeping a map from each original node to its clone.

The challenge is the cycles: an undirected graph has back-edges, so a naive
recursion would loop forever. The map serves two purposes:
  1. It tells us whether a node has already been cloned (so we reuse the clone
     instead of making a new one).
  2. It lets us wire up neighbor pointers to the cloned versions.

DFS version:
- If node is None, return None.
- If node is already in the map, return its clone.
- Otherwise create the clone, record it in the map BEFORE recursing (so cycles
  terminate), then recurse on each neighbor and append the cloned neighbors.

BFS version (same idea, queue instead of recursion): clone the start node, then
pop nodes from a queue; for each neighbor, clone it if unseen and append the
clone to the current clone's neighbor list.

Both visit each node and edge once.

Complexity
----------
- Time:  O(V + E), every node and edge processed once.
- Space: O(V) for the visited/clone map (plus recursion stack for DFS).

Python solution
---------------
class Solution:
    def cloneGraph(self, node):
        if node is None:
            return None

        clones = {}

        def dfs(cur):
            if cur in clones:
                return clones[cur]
            copy = Node(cur.val)
            clones[cur] = copy            # record before recursing -> handles cycles
            for nb in cur.neighbors:
                copy.neighbors.append(dfs(nb))
            return copy

        return dfs(node)

Interview tips
--------------
- The key insight is the hash map from original node -> clone; it both prevents
  infinite loops on cycles and de-duplicates shared neighbors.
- Insert the clone into the map BEFORE recursing into neighbors; otherwise a
  cycle re-enters the same node and recurses forever.
- Mention both DFS and BFS are valid; BFS avoids deep recursion stacks for large
  graphs.
- Edge cases: empty graph (None input) and a single isolated node.
- Use the node object itself as the map key (identity), or its unique val since
  the problem guarantees vals are unique.
"""
