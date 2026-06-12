# LeetCode #133 - Clone Graph

**Data structure:** Graph  
**Difficulty:** Medium  
**URL:** https://leetcode.com/problems/clone-graph/

## Problem

Given a reference of a node in a connected undirected graph, return a **deep copy** (clone) of the graph.

Each node contains a value (`int`) and a list of its neighbors:

```python
class Node:
    val: int
    neighbors: List[Node]
```

For the test format, each node's value equals its 1-indexed position, the graph is given as an adjacency list, and the supplied node is always the one with `val = 1`.

## Examples

```text
Input: adjList = [[2,4],[1,3],[2,4],[1,3]]
Output: [[2,4],[1,3],[2,4],[1,3]]
```

```text
Input: adjList = [[]]
Output: [[]]   (single node, no neighbors)
```

```text
Input: adjList = []
Output: []     (empty graph, given node is null)
```

## Constraints

- The number of nodes is in the range `[0, 100]`.
- `1 <= Node.val <= 100`, unique per node.
- No repeated edges and no self-loops.
- The graph is connected — all nodes reachable from the given node.

## Approach

Traverse the graph while keeping a map from each **original node → its clone**.

The challenge is the cycles: an undirected graph has back-edges, so naive recursion would loop forever. The map serves two purposes:

1. It tells us whether a node was already cloned (reuse the clone rather than re-creating it).
2. It lets us wire neighbor pointers to the cloned versions.

**DFS:**
- If `node` is `None`, return `None`.
- If `node` is already in the map, return its clone.
- Otherwise create the clone, record it in the map **before** recursing (so cycles terminate), then recurse on each neighbor and append the cloned neighbors.

A BFS variant uses a queue instead of recursion with the same map. Both visit each node and edge once.

**Complexity**

- Time: `O(V + E)` — every node and edge processed once
- Space: `O(V)` for the clone map (plus recursion stack for DFS)

## Python solution

```python
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
```

## unittest test cases

```python
import unittest


class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


def build_graph(adj_list):
    if not adj_list:
        return None
    nodes = {i + 1: Node(i + 1) for i in range(len(adj_list))}
    for i, neighbors in enumerate(adj_list):
        nodes[i + 1].neighbors = [nodes[n] for n in neighbors]
    return nodes[1]


def to_adj_list(node):
    if node is None:
        return []
    from collections import deque

    seen = {node.val: node}
    queue = deque([node])
    while queue:
        cur = queue.popleft()
        for nb in cur.neighbors:
            if nb.val not in seen:
                seen[nb.val] = nb
                queue.append(nb)
    return [sorted(nb.val for nb in seen[v].neighbors) for v in sorted(seen)]


def collect_ids(node):
    if node is None:
        return set()
    from collections import deque

    ids = {id(node)}
    queue = deque([node])
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

    def test_empty_graph(self):
        self.assertIsNone(self.sol.cloneGraph(None))

    def test_is_deep_copy(self):
        original = build_graph([[2, 4], [1, 3], [2, 4], [1, 3]])
        clone = self.sol.cloneGraph(original)
        self.assertEqual(collect_ids(original) & collect_ids(clone), set())

    def test_triangle_graph(self):
        original = build_graph([[2, 3], [1, 3], [1, 2]])
        clone = self.sol.cloneGraph(original)
        self.assertEqual(to_adj_list(clone), [[2, 3], [1, 3], [1, 2]])
```

## Interview tips

- The key insight is the map from original node → clone; it prevents infinite loops on cycles and de-duplicates shared neighbors.
- Insert the clone into the map **before** recursing into neighbors; otherwise a cycle re-enters the same node and recurses forever.
- Both DFS and BFS are valid; BFS avoids deep recursion stacks on large graphs.
- Edge cases: empty graph (`None` input) and a single isolated node.
- Use the node object itself as the map key (identity), or its unique `val` since the problem guarantees values are unique.
