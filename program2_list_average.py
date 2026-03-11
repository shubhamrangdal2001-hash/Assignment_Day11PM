"""
Program 2 – List Average Calculator (Refactored from Day 9)
Added: try/except/else/finally, input validation, specific exceptions
"""


def get_numbers_from_user():
    """Read a list of numbers typed by the user, one per line."""
    numbers = []
    print("Enter numbers one by one. Type 'done' when finished.\n")

    while True:
        try:
            raw = input("  Enter number (or 'done'): ").strip()

            if raw.lower() == "done":
                # Validate we have at least one number before stopping
                if len(numbers) == 0:
                    raise ValueError("You must enter at least one number before typing 'done'.")
                break

            value = float(raw)

            # Reject values that would break the calculation meaningfully
            if value != value:  # NaN check (float('nan'))
                raise ValueError("NaN is not a valid number.")

        except ValueError as e:
            print(f"  [Error] {e}. Try again.")

        else:
            # Runs only when the number was valid
            numbers.append(value)
            print(f"  Added {value}. List so far: {numbers}")

        finally:
            pass  # Nothing to clean up here, kept for structure

    return numbers


def calculate_average(numbers):
    """Calculate average with ZeroDivisionError guard."""
    try:
        total = sum(numbers)
        avg = total / len(numbers)

    except ZeroDivisionError:
        print("[Error] Cannot calculate average of an empty list.")
        return None

    else:
        return avg

    finally:
        print("\n  --- Calculation complete ---")


def main():
    print("=== List Average Calculator ===\n")

    try:
        numbers = get_numbers_from_user()
        avg = calculate_average(numbers)

        if avg is not None:
            print(f"\nNumbers entered : {numbers}")
            print(f"Count           : {len(numbers)}")
            print(f"Sum             : {sum(numbers)}")
            print(f"Average         : {avg:.2f}")
            print(f"Min             : {min(numbers)}")
            print(f"Max             : {max(numbers)}")

    except KeyboardInterrupt:
        print("\n\n[Info] Program interrupted by user. Exiting cleanly.")


if __name__ == "__main__":
    main()
