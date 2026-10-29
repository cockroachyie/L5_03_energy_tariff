# Static Analysis Issues — energy_system.py

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Use of `eval()` on user input | Security (High) | 63 | `eval(adjustment)` runs arbitrary Python code built from raw user input (`input()`), allowing code injection. Flagged by both Bandit (B307, Medium severity/High confidence) and Pylint (W0123). | Replace `eval()` with `ast.literal_eval()` if only numeric/literal expressions are needed, or write a small safe parser/validator (e.g. `float()`/`int()` with a try/except) that rejects anything that isn't a plain number. |
| Mutable default argument | Bug risk (Medium) | 12 | Function uses a mutable default value (`[]`) as a parameter default. Mutable defaults persist across calls and can cause subtle, hard-to-trace bugs when the list is modified. | Use `None` as the default and initialize the list inside the function body: `def f(data=None): data = data or []`. |
| Bare `except:` clause | Error handling (Medium) | 44 | Catches every exception, including unrelated ones (e.g. `KeyboardInterrupt`, `SystemExit`), hiding real bugs and making debugging harder. | Catch specific exceptions (e.g. `except (IOError, ValueError) as e:`) and log or handle them explicitly. |
| Use of `global` statement | Code smell (Medium) | 27, 40 | Functions mutate global state directly via `global`, making the code harder to test and reason about, and prone to unexpected side effects. | Refactor to pass state explicitly as function arguments/return values, or encapsulate the shared state in a class. |
| Files opened without `with` / explicit encoding | Reliability (Medium) | 42, 48 | `open()` is called without a context manager (risk of unclosed file handles on error) and without an explicit `encoding`, which can cause platform-dependent behavior. | Use `with open(path, "r", encoding="utf-8") as f:` (or `"w"`/`"a"` as appropriate) for all file I/O. |
| Unused import `sys` | Code quality (Low) | 2 | `sys` is imported but never used in the module. | Remove the unused `import sys` line. |
| Missing docstrings | Documentation (Low) | 1, 12, 17, 26, 32, 39, 47, 52 | Module and multiple functions lack docstrings, reducing readability and maintainability. | Add a module-level docstring and a short docstring to each function describing purpose, parameters, and return value. |
| Old-style string formatting | Style (Low) | 59, 60, 66 | Uses `%`-style or `.format()` string formatting instead of f-strings, which are more readable and performant. | Convert to f-strings, e.g. `f"{name}: {value}"`. |
| PEP 8 formatting violations | Style (Low) | 12, 17, 24, 26, 32, 39, 47, 52, 62, 68 | Missing blank lines between function/class definitions (E302/E305) and two lines exceeding the 79-character limit (E501). | Run `black` or `autopep8` to auto-format, or manually add the required blank lines and wrap long lines. |
| Unnecessary `elif` after `return` | Code smell (Low) | 19 | An `elif` follows a `return` statement, which is redundant since the `if` branch already exits the function. | Replace `elif` with a plain `if` at the same indentation level. |

## Summary
- **High severity:** 1 (eval injection)
- **Medium severity:** 4 (mutable default, bare except, global state, unsafe file handling)
- **Low severity:** 5 (unused import, missing docstrings, string formatting, PEP 8 style, redundant elif)

Overall Pylint score: **6.14/10**
