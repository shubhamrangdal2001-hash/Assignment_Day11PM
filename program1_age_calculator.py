"""
Program 1 – Age Calculator (Refactored from Day 8)
Added: try/except/else/finally, input validation with raise, logging
"""

import logging

# Set up logging – errors go to a file, user sees friendly messages only
logging.basicConfig(
    filename="age_calculator.log",
    level=logging.ERROR,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def get_valid_age():
    """Keep asking until the user enters a valid age."""
    while True:
        try:
            raw = input("Enter your age: ")
            age = int(raw)

            # Custom validation with raise
            if age < 0 or age > 150:
                raise ValueError(f"Age must be between 0 and 150, got {age}")

        except ValueError as e:
            logging.error("Invalid age input: %s | raw input: %s", e, raw)
            print(f"  Invalid input: {e}. Please try again.\n")

        else:
            # Only runs when no exception occurred
            print(f"  In 10 years you will be {age + 10} years old.")
            print(f"  In 10 years you were born in {2025 - age} approximately.")
            break

        finally:
            # Always runs – good place to clean up resources or show a separator
            print("  -" * 20)

    return age


def main():
    print("=== Age Calculator ===\n")
    age = get_valid_age()
    print(f"\nFinal answer: your age is {age}.")


if __name__ == "__main__":
    main()
