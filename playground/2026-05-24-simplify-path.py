"""LeetCode #71 — Simplify Path  (Stack · Medium)

URL: https://leetcode.com/problems/simplify-path/

Problem
-------
Given a string `path`, which is an absolute path (starting with a single slash
`/`) to a file or directory in a Unix-style file system, convert it to the
simplified canonical path. The canonical path must follow these rules:

  - Starts with a single slash '/'.
  - Any two directories are separated by a single slash '/'.
  - Does NOT end with a trailing '/'.
  - Contains only the directories on the path from the root to the target file
    or directory (i.e. no '.' or '..' elements).

A period '.' refers to the current directory. A double period '..' refers to
the directory up a level. Any multiple consecutive slashes ('//') are treated
as a single slash '/'.

Note: '...' (three or more dots) is treated as a regular directory name.

Examples
--------
  path = "/home/"                                 -> "/home"
  path = "/home//foo/"                            -> "/home/foo"
  path = "/home/user/Documents/../Pictures"       -> "/home/user/Pictures"
  path = "/../"                                   -> "/"
  path = "/.../a/../b/c/../d/./"                  -> "/.../b/d"

Constraints
-----------
  1 <= path.length <= 3000
  path consists of English letters, digits, period '.', slash '/' or '_'.
  path is a valid absolute Unix path.
  path begins with a slash '/'.

Run
---
  python 2026-05-24-simplify-path.py -v
"""

import unittest


class Solution:
    def simplifyPath(self, path):
        raise NotImplementedError("Implement simplifyPath")


# ----------------------------- tests -----------------------------

class TestSimplifyPath(unittest.TestCase):
    def setUp(self):
        self.s = Solution()

    def test_example1_trailing_slash(self):
        self.assertEqual(self.s.simplifyPath("/home/"), "/home")

    def test_example2_double_slash(self):
        self.assertEqual(self.s.simplifyPath("/home//foo/"), "/home/foo")

    def test_example3_parent_directory(self):
        self.assertEqual(
            self.s.simplifyPath("/home/user/Documents/../Pictures"),
            "/home/user/Pictures",
        )

    def test_example4_parent_at_root(self):
        # Going up from root stays at root.
        self.assertEqual(self.s.simplifyPath("/../"), "/")

    def test_example5_three_dots_is_a_name(self):
        # '...' is a valid directory name, NOT a special token.
        self.assertEqual(
            self.s.simplifyPath("/.../a/../b/c/../d/./"),
            "/.../b/d",
        )

    def test_root_only(self):
        self.assertEqual(self.s.simplifyPath("/"), "/")

    def test_many_consecutive_slashes(self):
        self.assertEqual(self.s.simplifyPath("///a///b/////c///"), "/a/b/c")

    def test_single_dot_segments(self):
        self.assertEqual(self.s.simplifyPath("/./././"), "/")

    def test_only_double_dots_collapses_to_root(self):
        self.assertEqual(self.s.simplifyPath("/../../../"), "/")

    def test_mixed_pop_and_push(self):
        # /a -> /a/b -> /a (pop b) -> /a/c -> / (pop a, pop c? trace it)
        # Trace: /a/b/../c/../..  =>  /a -> /a/b -> /a -> /a/c -> /a -> /
        self.assertEqual(self.s.simplifyPath("/a/b/../c/../.."), "/")

    def test_underscore_and_digits_in_name(self):
        self.assertEqual(
            self.s.simplifyPath("/var/log/app_2026/01/access.log"),
            "/var/log/app_2026/01/access.log",
        )

    def test_long_chain_no_simplification(self):
        self.assertEqual(
            self.s.simplifyPath("/etc/nginx/sites-enabled/default"),
            "/etc/nginx/sites-enabled/default",
        )

    def test_double_dots_then_real_name(self):
        # /a/b/../../c  =>  /c
        self.assertEqual(self.s.simplifyPath("/a/b/../../c"), "/c")

    def test_dot_adjacent_to_name(self):
        # '.hidden' is a regular name (only a bare '.' is the current-dir token).
        self.assertEqual(self.s.simplifyPath("/home/.hidden"), "/home/.hidden")


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  — peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
Classic stack / streaming pattern. Walk the path component-by-component and
maintain a stack of directory names that survive in the canonical answer.

  1. Split path on '/'. Because the string starts with '/' and may contain
     consecutive slashes, split('/') yields empty strings between them — that's
     fine, we filter them out in the loop.
  2. For each component c:
        - '' (empty)  -> skip (came from leading/double/trailing slash)
        - '.'         -> skip (no-op)
        - '..'        -> pop the stack if non-empty; otherwise we're at root,
                         do nothing (you cannot go above root)
        - anything else -> push c onto the stack (this is the only path where
                           '...' and '.hidden' fall through as regular names)
  3. The canonical path is '/' + '/'.join(stack).

No recursion, no DP, no length tricks — single pass with a stack.

Edge cases to verbalise
-----------------------
  - '/'        -> empty stack -> '/'
  - '/../'     -> '..' at root is a no-op, NOT an error
  - '/...'     -> three dots is NOT a special token; it's a directory name
  - '/.hidden' -> leading-dot filename is also a regular name
  - '////'     -> consecutive slashes collapse to one (handled by skipping
                 empty components after split)

Complexity
----------
- Time:  O(n)        each character is visited once during split + scan
- Space: O(n)        stack of components in the worst case (no '..'s)

Python solution
---------------
class Solution:
    def simplifyPath(self, path):
        stack = []
        for component in path.split('/'):
            if component == '' or component == '.':
                continue
            if component == '..':
                if stack:
                    stack.pop()
                continue
            stack.append(component)
        return '/' + '/'.join(stack)

Interview tips
--------------
- Lead with "I'll use a stack of surviving directory names." Naming the data
  structure up-front earns trust.
- Call out the four cases explicitly: empty, '.', '..', name. Most candidates
  forget the empty-string case that split('/') produces.
- '...' is the classic trap — interviewers love to ask 'why didn't you treat
  three dots specially?' The answer: the spec only defines '.' and '..'.
- '..' at root is a no-op, NOT an error. Mention this before coding.
- Time/space O(n). The stack version is strictly cleaner than trying to mutate
  the string in place with a two-pointer scan — don't get clever.
- If asked to extend to relative paths (no leading '/'), the same stack works;
  just don't prepend '/' at the end and treat the first '..' as 'go up from
  cwd' instead of a no-op.
"""
