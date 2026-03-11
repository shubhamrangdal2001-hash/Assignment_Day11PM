"""
Part C – Interview Ready
Q2: safe_json_load(filepath)
Q3: Fixed process_data() function
"""

import json
import logging
from pathlib import Path

logging.basicConfig(
    filename="part_c.log",
    level=logging.ERROR,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


# ─────────────────────────────────────────────
# Q2 – safe_json_load(filepath)
# ─────────────────────────────────────────────

def safe_json_load(filepath):
    """
    Safely read and parse a JSON file.
    Returns the parsed dict on success, None on any failure.
    Logs all errors to part_c.log.
    """
    try:
        path = Path(filepath)
        with open(path, "r") as f:
            data = json.load(f)

    except FileNotFoundError as e:
        logging.error("File not found: %s | %s", filepath, e)
        print(f"  [Error] File not found: {filepath}")
        return None

    except json.JSONDecodeError as e:
        logging.error("Invalid JSON in %s: %s", filepath, e)
        print(f"  [Error] File is not valid JSON: {e.msg} at line {e.lineno}")
        return None

    except PermissionError as e:
        logging.error("Permission denied reading %s: %s", filepath, e)
        print(f"  [Error] Permission denied: {filepath}")
        return None

    else:
        # Runs only when no exception was raised
        print(f"  [OK] Loaded {filepath} successfully.")
        return data

    finally:
        # Always runs – could close resources here
        print(f"  [Info] Attempted to load: {filepath}")


# ─────────────────────────────────────────────
# Q3 – Fixed process_data()
# ─────────────────────────────────────────────
# Bug 1: bare except → changed to except (ValueError, TypeError)
# Bug 2: return inside finally → moved return out of finally block
# Bug 3: vague error message → print the item and exception detail

def process_data(data_list):
    """
    Process a list of items, converting each to int and doubling it.
    Skips items that cannot be converted.
    """
    results = []

    for item in data_list:
        try:
            value = int(item)
            results.append(value * 2)

        except (ValueError, TypeError) as e:
            # Fix 1: Specific exceptions instead of bare except
            # Fix 3: Informative error message
            print(f"  [Skipped] Could not convert '{item}' to int: {e}")
            continue

        # Fix 2: 'finally' block removed – it was forcing an early return
        # The return statement belongs OUTSIDE the loop

    return results  # Now correctly runs after all iterations


# ─────────────────────────────────────────────
# Demo
# ─────────────────────────────────────────────

if __name__ == "__main__":
    # --- Q2 demo ---
    print("=== Q2: safe_json_load Demo ===\n")

    # Create a valid JSON file to test with
    with open("valid_data.json", "w") as f:
        json.dump({"name": "Alice", "score": 95}, f)

    # Create a broken JSON file
    with open("broken_data.json", "w") as f:
        f.write("{name: Alice, score: 95")  # missing quotes = invalid

    result1 = safe_json_load("valid_data.json")
    print(f"  Result: {result1}\n")

    result2 = safe_json_load("broken_data.json")
    print(f"  Result: {result2}\n")

    result3 = safe_json_load("nonexistent.json")
    print(f"  Result: {result3}\n")

    # --- Q3 demo ---
    print("=== Q3: process_data Demo ===\n")
    test_input = ["3", "7", "abc", None, "5", "10.5", "2"]
    output = process_data(test_input)
    print(f"\n  Input : {test_input}")
    print(f"  Output: {output}")
