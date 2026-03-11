"""
Part B – Resilient File Processor with Retry Logic
Reads a directory of CSV files, handles corrupted/empty/wrong-format files,
retries on PermissionError, exports processing_report.json.
"""

import csv
import json
import logging
import time
import traceback
from pathlib import Path
from datetime import datetime

# Logging – full tracebacks go to file, summary to screen
logging.basicConfig(
    filename="file_processor.log",
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds between retries


def parse_csv_file(filepath):
    """
    Parse a CSV file and return rows as list of dicts.
    Raises ValueError for empty or wrong-format files.
    """
    rows = []

    with open(filepath, "r", newline="") as f:
        content = f.read().strip()

    if not content:
        raise ValueError("File is empty.")

    # Try parsing with DictReader
    with open(filepath, "r", newline="") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames

        if not headers:
            raise ValueError("File has no headers.")

        for row in reader:
            rows.append(dict(row))

    if len(rows) == 0:
        raise ValueError("File has headers but no data rows.")

    return rows


def calculate_aggregates(rows, filepath_name):
    """
    Try to compute numeric aggregates from the rows.
    Returns a summary dict.
    """
    numeric_cols = {}

    for row in rows:
        for key, val in row.items():
            try:
                numeric_cols.setdefault(key, []).append(float(val))
            except (ValueError, TypeError):
                pass  # skip non-numeric fields

    aggregates = {}
    for col, values in numeric_cols.items():
        if values:
            aggregates[col] = {
                "count": len(values),
                "sum": round(sum(values), 2),
                "average": round(sum(values) / len(values), 2),
                "min": min(values),
                "max": max(values),
            }

    return {"row_count": len(rows), "aggregates": aggregates}


def process_file_with_retry(filepath):
    """
    Attempt to process a single file.
    Retries up to MAX_RETRIES times on PermissionError.
    Returns (success: bool, result_or_error: dict or str)
    """
    attempts = 0

    while attempts < MAX_RETRIES:
        attempts += 1
        try:
            logging.info("Processing: %s (attempt %d)", filepath.name, attempts)
            rows = parse_csv_file(filepath)
            summary = calculate_aggregates(rows, filepath.name)
            return True, summary

        except PermissionError as e:
            logging.warning(
                "PermissionError on %s attempt %d: %s", filepath.name, attempts, e
            )
            if attempts < MAX_RETRIES:
                print(f"  [Permission Denied] {filepath.name} – retrying in {RETRY_DELAY}s "
                      f"(attempt {attempts}/{MAX_RETRIES})")
                time.sleep(RETRY_DELAY)
            else:
                tb = traceback.format_exc()
                logging.error("Failed after %d attempts: %s\n%s", MAX_RETRIES, filepath.name, tb)
                return False, f"PermissionError after {MAX_RETRIES} attempts: {e}"

        except (ValueError, csv.Error) as e:
            tb = traceback.format_exc()
            logging.error("Parse error in %s: %s\n%s", filepath.name, e, tb)
            return False, str(e)

        except Exception as e:
            tb = traceback.format_exc()
            logging.error("Unexpected error in %s: %s\n%s", filepath.name, e, tb)
            return False, f"Unexpected error: {e}"

    return False, "Max retries exceeded"


def process_directory(directory):
    """Process all CSV files in the given directory."""
    dir_path = Path(directory)

    if not dir_path.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")

    csv_files = list(dir_path.glob("*.csv"))

    if not csv_files:
        print(f"No CSV files found in {directory}.")
        return

    print(f"Found {len(csv_files)} CSV file(s) in '{directory}'\n")

    files_processed = 0
    files_failed = 0
    error_details = {}
    results = {}

    for filepath in sorted(csv_files):
        print(f"Processing: {filepath.name} ...", end=" ")
        success, data = process_file_with_retry(filepath)

        if success:
            files_processed += 1
            results[filepath.name] = data
            print(f"OK  (rows: {data['row_count']})")
        else:
            files_failed += 1
            error_details[filepath.name] = data
            print(f"FAILED  ({data})")

    # Build and export report
    report = {
        "metadata": {
            "generated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "directory": str(dir_path.resolve()),
            "files_found": len(csv_files),
            "files_processed": files_processed,
            "files_failed": files_failed,
        },
        "results": results,
        "error_details": error_details,
    }

    report_path = "processing_report.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\nReport saved to {report_path}")
    print(f"Processed: {files_processed} | Failed: {files_failed}")
    return report


def create_sample_files(folder):
    """Create sample CSV files for testing (good, empty, corrupted, wrong format)."""
    folder = Path(folder)
    folder.mkdir(exist_ok=True)

    # Good file
    with open(folder / "sales_jan.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "product", "qty", "price"])
        writer.writerows([
            ["2025-01-01", "Laptop", "3", "45000"],
            ["2025-01-02", "Mouse",  "10", "600"],
            ["2025-01-03", "Keyboard", "5", "1200"],
        ])

    # Another good file
    with open(folder / "sales_feb.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "product", "qty", "price"])
        writer.writerows([
            ["2025-02-01", "Monitor", "2", "22000"],
            ["2025-02-02", "Laptop",  "1", "45000"],
        ])

    # Empty file
    with open(folder / "empty_file.csv", "w") as f:
        f.write("")

    # Wrong format (only header, no rows)
    with open(folder / "header_only.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "product", "qty", "price"])

    # Corrupted / non-CSV text
    with open(folder / "corrupted.csv", "w") as f:
        f.write("THIS IS NOT A VALID CSV FILE !!!\n@@@@###$$$\n")

    print(f"Sample files created in '{folder}/'")


if __name__ == "__main__":
    sample_dir = "sample_csv_files"
    create_sample_files(sample_dir)
    print()
    process_directory(sample_dir)
