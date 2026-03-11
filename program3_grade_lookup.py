"""
Program 3 – Student Grade Lookup (Refactored from Day 10)
Added: try/except/else/finally, raise with custom messages, specific exceptions
"""

import logging

logging.basicConfig(
    filename="grade_lookup.log",
    level=logging.WARNING,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# Sample student records – simulates a data store
STUDENT_DB = {
    "alice": {"math": 88, "english": 92, "science": 79},
    "bob":   {"math": 55, "english": 60, "science": 70},
    "carol": {"math": 95, "english": 91, "science": 97},
    "dave":  {"math": 40, "english": 55, "science": 50},
}


def lookup_grade(student_name, subject):
    """
    Fetch a student's grade for a given subject.
    Raises KeyError if student or subject is not found.
    """
    name_lower = student_name.strip().lower()
    subject_lower = subject.strip().lower()

    try:
        student_record = STUDENT_DB[name_lower]

    except KeyError:
        msg = f"Student '{student_name}' not found in database."
        logging.warning("Lookup failed: %s", msg)
        raise KeyError(msg)

    try:
        grade = student_record[subject_lower]

    except KeyError:
        available = ", ".join(student_record.keys())
        msg = f"Subject '{subject}' not found for {student_name}. Available: {available}"
        logging.warning("Lookup failed: %s", msg)
        raise KeyError(msg)

    return grade


def grade_to_letter(grade):
    """Convert numeric grade to letter grade."""
    if not isinstance(grade, (int, float)):
        raise TypeError(f"Grade must be a number, got {type(grade).__name__}")
    if grade < 0 or grade > 100:
        raise ValueError(f"Grade must be between 0 and 100, got {grade}")

    if grade >= 90:
        return "A"
    elif grade >= 75:
        return "B"
    elif grade >= 60:
        return "C"
    elif grade >= 50:
        return "D"
    else:
        return "F"


def main():
    print("=== Student Grade Lookup ===")
    print("Available students:", ", ".join(STUDENT_DB.keys()))
    print("Available subjects: math, english, science\n")

    while True:
        try:
            student = input("Enter student name (or 'quit'): ").strip()
            if student.lower() == "quit":
                print("Goodbye!")
                break

            if not student:
                raise ValueError("Student name cannot be empty.")

            subject = input("Enter subject: ").strip()
            if not subject:
                raise ValueError("Subject cannot be empty.")

            grade = lookup_grade(student, subject)

        except KeyError as e:
            print(f"  [Not Found] {e}\n")

        except ValueError as e:
            print(f"  [Invalid Input] {e}\n")

        else:
            # Only runs when no exception
            letter = grade_to_letter(grade)
            print(f"\n  {student.title()} | {subject.title()} | Grade: {grade} ({letter})\n")

        finally:
            print("  " + "-" * 40)


if __name__ == "__main__":
    main()
