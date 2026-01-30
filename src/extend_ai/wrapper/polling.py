"""
Polling utilities with exponential backoff and proportional jitter.

Example:
    # Polls until complete
    result = poll_until_done(
        retrieve=lambda: client.extract_runs.retrieve(id),
        is_terminal=lambda res: res.extract_run.status != "PROCESSING"
    )

    # With custom timeout
    result = poll_until_done(
        retrieve=lambda: client.extract_runs.retrieve(id),
        is_terminal=lambda res: res.extract_run.status != "PROCESSING",
        options=PollingOptions(max_wait_ms=300000)  # 5 minute timeout
    )
"""

import asyncio
import random
import time
from dataclasses import dataclass
from typing import Awaitable, Callable, Optional, TypeVar

T = TypeVar("T")


@dataclass
class PollingOptions:
    """
    Configuration options for polling behavior.

    Attributes:
        max_wait_ms: Maximum total wait time in milliseconds. Default: None (polls indefinitely).
        initial_delay_ms: Initial delay between polls in milliseconds. Default: 1000 (1 second).
        max_delay_ms: Maximum delay between polls in milliseconds. Default: 60000 (60 seconds).
        jitter_fraction: Jitter fraction for randomization. A value of 0.25 means delays
            will be randomized by +/-25%. Default: 0.25.
    """

    max_wait_ms: Optional[int] = None  # None = poll indefinitely
    initial_delay_ms: int = 1_000  # 1 second
    max_delay_ms: int = 60_000  # 60 seconds
    jitter_fraction: float = 0.25


class PollingTimeoutError(Exception):
    """Error thrown when polling exceeds the maximum wait time."""

    def __init__(self, message: str, elapsed_ms: int, max_wait_ms: int):
        super().__init__(message)
        self.elapsed_ms = elapsed_ms
        self.max_wait_ms = max_wait_ms


def calculate_backoff_delay(
    attempt: int,
    initial_delay_ms: int,
    max_delay_ms: int,
    jitter_fraction: float,
) -> int:
    """
    Calculates the next delay using exponential backoff with proportional jitter.

    Args:
        attempt: The current attempt number (0-indexed)
        initial_delay_ms: The base delay for the first attempt
        max_delay_ms: The maximum delay cap
        jitter_fraction: The fraction of delay to randomize (+/-)

    Returns:
        The delay in milliseconds
    """
    # Exponential backoff: initialDelay * 2^attempt
    exponential_delay = initial_delay_ms * (2**attempt)

    # Cap at maxDelay
    capped_delay = min(exponential_delay, max_delay_ms)

    # Apply proportional jitter: delay * (1 + random(-jitterFraction, +jitterFraction))
    jitter = (random.random() * 2 - 1) * jitter_fraction
    final_delay = capped_delay * (1 + jitter)

    return round(final_delay)


def poll_until_done(
    retrieve: Callable[[], T],
    is_terminal: Callable[[T], bool],
    options: Optional[PollingOptions] = None,
) -> T:
    """
    Polls a retrieve function until a terminal condition is met (synchronous version).

    Uses exponential backoff with proportional jitter to avoid thundering herd
    problems and reduce load on the server.

    Args:
        retrieve: Function that fetches the current state
        is_terminal: Predicate that returns True when polling should stop
        options: Polling configuration options

    Returns:
        The final result when is_terminal returns True

    Raises:
        PollingTimeoutError: If max_wait_ms is set and exceeded

    Example:
        result = poll_until_done(
            retrieve=lambda: client.extract_runs.retrieve(run_id),
            is_terminal=lambda res: res.extract_run.status != "PROCESSING"
        )
    """
    if options is None:
        options = PollingOptions()

    max_wait_ms = options.max_wait_ms
    initial_delay_ms = options.initial_delay_ms
    max_delay_ms = options.max_delay_ms
    jitter_fraction = options.jitter_fraction

    start_time = time.time() * 1000  # Convert to milliseconds
    attempt = 0

    while True:
        result = retrieve()

        if is_terminal(result):
            return result

        elapsed_ms = (time.time() * 1000) - start_time

        # Only check timeout if max_wait_ms is set
        if max_wait_ms is not None and elapsed_ms >= max_wait_ms:
            raise PollingTimeoutError(
                f"Polling timed out after {int(elapsed_ms)}ms (max: {max_wait_ms}ms)",
                int(elapsed_ms),
                max_wait_ms,
            )

        delay = calculate_backoff_delay(attempt, initial_delay_ms, max_delay_ms, jitter_fraction)

        # If timeout is set, don't wait longer than remaining time
        if max_wait_ms is not None:
            remaining_ms = max_wait_ms - elapsed_ms
            actual_delay = min(delay, remaining_ms)
        else:
            actual_delay = delay

        time.sleep(actual_delay / 1000)  # Convert to seconds for time.sleep
        attempt += 1


async def poll_until_done_async(
    retrieve: Callable[[], Awaitable[T]],
    is_terminal: Callable[[T], bool],
    options: Optional[PollingOptions] = None,
) -> T:
    """
    Polls a retrieve function until a terminal condition is met (asynchronous version).

    Uses exponential backoff with proportional jitter to avoid thundering herd
    problems and reduce load on the server.

    Args:
        retrieve: Async function that fetches the current state
        is_terminal: Predicate that returns True when polling should stop
        options: Polling configuration options

    Returns:
        The final result when is_terminal returns True

    Raises:
        PollingTimeoutError: If max_wait_ms is set and exceeded

    Example:
        result = await poll_until_done_async(
            retrieve=lambda: client.extract_runs.retrieve(run_id),
            is_terminal=lambda res: res.extract_run.status != "PROCESSING"
        )
    """
    if options is None:
        options = PollingOptions()

    max_wait_ms = options.max_wait_ms
    initial_delay_ms = options.initial_delay_ms
    max_delay_ms = options.max_delay_ms
    jitter_fraction = options.jitter_fraction

    start_time = time.time() * 1000  # Convert to milliseconds
    attempt = 0

    while True:
        result = await retrieve()

        if is_terminal(result):
            return result

        elapsed_ms = (time.time() * 1000) - start_time

        # Only check timeout if max_wait_ms is set
        if max_wait_ms is not None and elapsed_ms >= max_wait_ms:
            raise PollingTimeoutError(
                f"Polling timed out after {int(elapsed_ms)}ms (max: {max_wait_ms}ms)",
                int(elapsed_ms),
                max_wait_ms,
            )

        delay = calculate_backoff_delay(attempt, initial_delay_ms, max_delay_ms, jitter_fraction)

        # If timeout is set, don't wait longer than remaining time
        if max_wait_ms is not None:
            remaining_ms = max_wait_ms - elapsed_ms
            actual_delay = min(delay, remaining_ms)
        else:
            actual_delay = delay

        await asyncio.sleep(actual_delay / 1000)  # Convert to seconds for asyncio.sleep
        attempt += 1
