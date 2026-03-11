# Error Handling Checklist

## Program 1 – Age Calculator (`program1_age_calculator.py`)

| # | Exception Caught | Recovery Action | User Sees | Logged |
|---|---|---|---|---|
| 1 | `ValueError` (non-integer input) | Print message, loop again | "Invalid input: ... Please try again." | Yes – to `age_calculator.log` |
| 2 | `ValueError` (age out of range 0–150) | Print message, loop again | "Invalid input: Age must be between 0 and 150, got X." | Yes – to `age_calculator.log` |

**`finally` block:** Prints a separator line `------` after every attempt regardless of success or failure.  
**`else` block:** Prints the result and breaks the loop only when input is valid.

---

## Program 2 – List Average Calculator (`program2_list_average.py`)

| # | Exception Caught | Recovery Action | User Sees | Logged |
|---|---|---|---|---|
| 1 | `ValueError` (non-numeric input) | Print message, loop continues | "[Error] ... Try again." | No (user-facing only) |
| 2 | `ValueError` (done before any number) | Print message, prompt again | "[Error] Must enter at least one number." | No |
| 3 | `ZeroDivisionError` (empty list avg) | Return `None`, skip print | "[Error] Cannot calculate average of empty list." | No |
| 4 | `KeyboardInterrupt` (Ctrl+C) | Exit cleanly | "Program interrupted by user. Exiting cleanly." | No |

**`else` block:** Appends the valid number and confirms it was added.  
**`finally` block:** Separator after calculation (structural).

---

## Program 3 – Student Grade Lookup (`program3_grade_lookup.py`)

| # | Exception Caught | Recovery Action | User Sees | Logged |
|---|---|---|---|---|
| 1 | `KeyError` (student not found) | Skip, prompt again | "[Not Found] Student 'X' not found in database." | Yes – `WARNING` to `grade_lookup.log` |
| 2 | `KeyError` (subject not found) | Skip, prompt again | "[Not Found] Subject 'X' not found. Available: ..." | Yes – `WARNING` to `grade_lookup.log` |
| 3 | `ValueError` (empty input) | Skip, prompt again | "[Invalid Input] Name/subject cannot be empty." | No |
| 4 | `TypeError` in `grade_to_letter()` | Raised to caller | Would display as ValueError/TypeError message | No |

**`else` block:** Displays the grade result only when lookup succeeds.  
**`finally` block:** Always prints a separator line after each query.

---

## Notes on Exception Design

- **No bare `except:` used anywhere** – all blocks use specific exception types.
- **`raise` with custom messages** used in `lookup_grade()` and `get_valid_age()` for meaningful feedback.
- **Logging** separates internal debug info from user-facing messages in Programs 1 and 3.
- **`else` block** is used to confirm "happy path" actions only run on success.
- **`finally` block** is used for cleanup or separators that must always execute.
