"""
Part D – AI-Augmented Task
@retry decorator with exponential backoff.
Prompt used: "Write a Python decorator called @retry(max_attempts=3, delay=1)
that automatically retries a function if it raises an exception,
with exponential backoff."
"""

import time
import random
import functools
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


# ─────────────────────────────────────────────
# AI-Generated Decorator (with minor test additions)
# ─────────────────────────────────────────────

def retry(max_attempts=3, delay=1, exceptions=(Exception,)):
    """
    Decorator factory that retries a function on exception.
    Uses exponential backoff: delay * 2^(attempt-1)
    
    Parameters:
        max_attempts : int  – maximum number of tries
        delay        : int  – base delay in seconds (doubles each retry)
        exceptions   : tuple – which exceptions to catch and retry on
    """
    def decorator(func):
        @functools.wraps(func)   # preserves __name__, __doc__ etc.
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(1, max_attempts + 1):
                try:
                    result = func(*args, **kwargs)
                    logging.info("'%s' succeeded on attempt %d", func.__name__, attempt)
                    return result

                except exceptions as e:
                    last_exception = e
                    wait = delay * (2 ** (attempt - 1))  # exponential backoff
                    logging.warning(
                        "'%s' failed on attempt %d/%d: %s. Waiting %.1fs before retry.",
                        func.__name__, attempt, max_attempts, e, wait
                    )

                    if attempt < max_attempts:
                        time.sleep(wait)

            # All attempts exhausted – re-raise the last exception
            logging.error(
                "'%s' failed after %d attempts. Last error: %s",
                func.__name__, max_attempts, last_exception
            )
            raise last_exception

        return wrapper
    return decorator


# ─────────────────────────────────────────────
# Test: function that fails ~50% of the time
# ─────────────────────────────────────────────

@retry(max_attempts=3, delay=1)
def unstable_fetch(resource_id):
    """Simulates a network call that randomly fails 50% of the time."""
    if random.random() < 0.5:
        raise ConnectionError(f"Failed to fetch resource '{resource_id}' (simulated network error)")
    return f"Data for resource '{resource_id}'"


# Test with only ValueError retries – ConnectionError will NOT be retried
@retry(max_attempts=3, delay=1, exceptions=(ValueError,))
def strict_function(value):
    """Only retries on ValueError, not on ConnectionError."""
    if value < 0:
        raise ValueError(f"Value must be positive, got {value}")
    if value == 0:
        raise ConnectionError("Zero is not allowed (non-retryable)")
    return value * 10


# ─────────────────────────────────────────────
# Demo
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Part D: @retry Decorator Demo ===\n")

    # Test 1: unstable_fetch – retries on any Exception
    print("--- Test 1: unstable_fetch (50% failure rate) ---")
    random.seed(42)  # fixed seed so output is reproducible in demo
    for i in range(3):
        try:
            result = unstable_fetch(f"item_{i}")
            print(f"  Success: {result}\n")
        except ConnectionError as e:
            print(f"  All retries exhausted: {e}\n")

    # Test 2: verify functools.wraps preserved metadata
    print("--- Test 2: functools.wraps check ---")
    print(f"  Function name : {unstable_fetch.__name__}")
    print(f"  Docstring     : {unstable_fetch.__doc__}\n")

    # Test 3: strict_function – only retries ValueError
    print("--- Test 3: Non-retryable exception (ConnectionError) ---")
    try:
        strict_function(0)
    except ConnectionError as e:
        print(f"  Correctly raised immediately (no retry): {e}\n")

    # Test 4: retryable exception
    print("--- Test 4: Retryable ValueError ---")
    try:
        strict_function(-5)
    except ValueError as e:
        print(f"  ValueError after 3 attempts: {e}\n")
