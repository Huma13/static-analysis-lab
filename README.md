# Lab 5: Static Code Analysis

Script analysed: `inventory_system.py` (tools: Pylint, Bandit, Flake8)

| Tool | Before | After |
|------|--------|-------|
| Pylint | 5.87 / 10 | 10.00 / 10 |
| Bandit | 1 High, 1 Medium, 4 Low | 0 issues |
| Flake8 | 18 findings | 0 findings |

Reports are in `reports/` (`*_before.txt` and `*_after.txt`).

## Issue table

| Issue | Type | Line(s) (original) | Description | Fix approach |
|-------|------|--------------------|-------------|--------------|
| `subprocess.call(..., shell=True)` (B602) | Security (High) | 52 | Command string built from input; shell injection risk | Removed the shell call; the report is printed with plain Python |
| `eval(expression)` (B307) | Security (Medium) | 55 | Arbitrary code execution | Replaced with an `ast`-based evaluator that allows only numbers and + - * / |
| Hardcoded password `ADMIN_PASSWORD = "admin123"` (B105) | Security (Low) | 8 | Secret in source code | Read from the `ADMIN_PASSWORD` environment variable |
| `pickle` import and use (B403) | Security (Low) | 4, 49 | Pickle can run code when loading untrusted data | Backup now written as JSON |
| `except: pass` (B110) | Security / Bug | 22-23 | Bare except silently hides every error | Catch `KeyError` only and print a message |
| Mutable default argument `logs=[]` (W0102) | Bug | 10 | The list is shared across all calls | Default to `None`, create a new list inside |
| `== None` (E711) | Style | 11 | Should use identity comparison | Changed to `is None` |
| Missing blank lines (E302/E305) | Style | many | PEP 8 needs 2 blank lines around functions | Added blank lines |
| `open()` without `with` (R1732) | Quality | 36, 43 | File may stay open if an error occurs | Used `with open(..., encoding="utf-8")` |
| Missing docstrings (C0114/C0116) | Quality | all | No documentation | Added module and function docstrings |
| Unused import `sys` (F401) | Style | 2 | Dead code | Removed |
| Crash on `add_item(123, "ten")` | Bug | 14 | `TypeError` when adding int + str | Validate types, raise `ValueError`, handled in `main()` |

## Reflection

**1. Which issues were the easiest to fix, and which were the hardest?**
The easiest were the Flake8 style issues (blank lines, spacing, `is None`, the unused import) and the missing docstrings, since they are mechanical. The hardest was `eval`, because there is no one-line replacement: `ast.literal_eval` cannot evaluate `2 + 3`, so I wrote a small safe evaluator. Removing `shell=True` and `pickle` also needed a design decision.

**2. Did the tools report any false positives?**
Not serious ones. Some Bandit findings (B403 for importing `pickle`, B105 for a password-like string) are Low severity and would be fine in a throwaway script. They still point at real risks in production code, so I fixed them rather than suppressing them. If a finding is a deliberate and safe choice, the right way to silence it is a justified `# nosec` or `# pylint: disable=` comment.

**3. How would you integrate static analysis into a real workflow?**
Run the tools locally with a pre-commit hook, and again in CI (for example GitHub Actions) on every pull request. Set the build to fail on Bandit High/Medium findings, any Flake8 error, and a Pylint score below a threshold such as 9.0. Keep the config (`.flake8`, `.pylintrc`) in the repo so everyone gets the same results.

**4. What tangible improvements did you see in code quality and security?**
Pylint went from 5.87 to 10.00 and Bandit from 6 findings (including a High) to none. The code is safer (no `eval`, no shell, no pickle, no hardcoded secret), more robust (no shared mutable default, no silent `except: pass`, input validation fixes a real crash), and easier to read and maintain (docstrings, PEP 8 formatting, f-strings, context managers).
