# DSA Daily — Playground

**One `.py` per question.** Each file is your practice surface AND the reference solution, so there are no duplicate files to keep in sync.

## File structure

```
"""Problem statement, examples, constraints, run command"""

import unittest

class Solution:
    def someMethod(self, args):
        raise NotImplementedError(...)         # ← write your code here

class TestSomething(unittest.TestCase):
    ...                                        # ← these tests must pass

if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  — peek only if stuck
# ============================================================================

REFERENCE = """
Approach, complexity, canonical Python solution, interview tips...
"""
```

## Workflow

```powershell
cd C:\Users\bhushanidhi\.copilot\skills\dsa-daily\playground

# Tests will all fail with NotImplementedError until you implement Solution
python 2026-05-03-3sum.py -v

# Implement, re-run, iterate
```

## Peeking at the reference

The bottom-of-file `REFERENCE` string holds the approach, complexity, canonical solution, and interview tips. To read it:

```powershell
# Just scroll to the bottom of the file, OR
python -c "import importlib.util, sys; spec = importlib.util.spec_from_file_location('q','2026-05-03-3sum.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); print(m.REFERENCE)"
```

…though honestly just scrolling is easier.

## Conventions

- Each file is self-contained — no imports between playground files.
- **No type annotations** in signatures or variables — clean `def f(self, nums):` style.
- Helper functions (e.g. `list_to_linked`, `build_tree`) are inlined per file.
- The `REFERENCE` string at the bottom is a single triple-quoted block; it is NOT executed, just stored for reading.

## File naming

`<YYYY-MM-DD>-<leetcode-slug>.py`

## When you're done

Once all tests pass, your implementation matches the canonical behaviour. Compare your code against the `REFERENCE` block to see alternative approaches and complexity notes.
