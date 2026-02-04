"""
Polling utilities with hybrid polling strategy: fast initial polls followed
by exponential backoff with proportional jitter.

The default strategy polls at 1-second intervals for the first 30 seconds,
then gradually increases the interval using exponential backoff (1.15x multiplier)
up to a maximum of 30 seconds between polls.

Example:
    # Polls until complete (uses hybrid strategy by default)
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

    # Custom fast polling phase
    result = poll_until_done(
        retrieve=lambda: client.extract_runs.retrieve(id),
        is_terminal=lambda res: res.extract_run.status != "PROCESSING",
        options=PollingOptions(
            fast_poll_duration_ms=60000,  # Fast poll for 60 seconds
            fast_poll_interval_ms=500,    # Poll every 500ms during fast phase
        )
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
        fast_poll_duration_ms: Duration of the fast polling phase in milliseconds.
            During this phase, polls occur at a fixed interval (fast_poll_interval_ms).
            Default: 30000 (30 seconds).
        fast_poll_interval_ms: Interval between polls during the fast polling phase
            in milliseconds. Default: 1000 (1 second).
        initial_delay_ms: Initial delay for the backoff phase (after fast polling ends)
            in milliseconds. Default: 1000 (1 second).
        max_delay_ms: Maximum delay between polls in milliseconds. Default: 30000 (30 seconds).
        backoff_multiplier: Multiplier for exponential backoff during the backoff phase.
            A value of 1.15 means each delay is 1.15x the previous delay. Default: 1.15.
        jitter_fraction: Jitter fraction for randomization. A value of 0.25 means delays
            will be randomized by +/-25%. Default: 0.25.
    """

    max_wait_ms: Optional[int] = None  # None = poll indefinitely
    fast_poll_duration_ms: int = 30_000  # 30 seconds
    fast_poll_interval_ms: int = 1_000  # 1 second
    initial_delay_ms: int = 1_000  # 1 second
    max_delay_ms: int = 30_000  # 30 seconds
    backoff_multiplier: float = 1.15
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
    backoff_multiplier: float = 2.0,
) -> int:
    """
    Calculates the next delay using exponential backoff with proportional jitter.

    Args:
        attempt: The current attempt number (0-indexed)
        initial_delay_ms: The base delay for the first attempt
        max_delay_ms: The maximum delay cap
        jitter_fraction: The fraction of delay to randomize (+/-)
        backoff_multiplier: The multiplier for exponential backoff (default: 2)

    Returns:
        The delay in milliseconds
    """
    # Exponential backoff: initialDelay * multiplier^attempt
    exponential_delay = initial_delay_ms * (backoff_multiplier**attempt)

    # Cap at maxDelay
    capped_delay = min(exponential_delay, max_delay_ms)

    # Apply proportional jitter: delay * (1 + random(-jitterFraction, +jitterFraction))
    jitter = (random.random() * 2 - 1) * jitter_fraction
    final_delay = capped_delay * (1 + jitter)

    return round(final_delay)


@dataclass
class HybridDelayOptions:
    """Configuration options for calculating hybrid delay."""

    fast_poll_duration_ms: int
    fast_poll_interval_ms: int
    initial_delay_ms: int
    max_delay_ms: int
    backoff_multiplier: float
    jitter_fraction: float


def calculate_hybrid_delay(elapsed_ms: float, options: HybridDelayOptions) -> int:
    """
    Calculates the delay for a hybrid polling strategy based on elapsed time.

    During the fast polling phase (elapsed < fast_poll_duration_ms), returns a fixed
    interval with jitter. After the fast phase ends, switches to exponential backoff.

    Args:
        elapsed_ms: Total elapsed time since polling started
        options: Configuration options for the hybrid strategy

    Returns:
        The delay in milliseconds until the next poll
    """
    # Fast polling phase: use fixed interval with jitter
    if elapsed_ms < options.fast_poll_duration_ms:
        jitter = (random.random() * 2 - 1) * options.jitter_fraction
        return round(options.fast_poll_interval_ms * (1 + jitter))

    # Backoff phase: calculate attempt number based on time since fast phase ended
    time_since_backoff_start = elapsed_ms - options.fast_poll_duration_ms

    # Calculate which "attempt" we're on based on elapsed time in backoff phase
    # Sum of geometric series: S = a * (r^n - 1) / (r - 1)
    # Solving for n: n = log((S * (r - 1) / a) + 1) / log(r)
    if options.backoff_multiplier == 1:
        # Linear case: attempt = time_since_backoff_start / initial_delay_ms
        attempt = int(time_since_backoff_start / options.initial_delay_ms)
    else:
        import math

        r = options.backoff_multiplier
        a = options.initial_delay_ms
        s = time_since_backoff_start

        # Estimate attempt from geometric series sum formula
        inner_value = (s * (r - 1)) / a + 1
        if inner_value <= 0:
            attempt = 0
        else:
            attempt = int(math.log(inner_value) / math.log(r))

    return calculate_backoff_delay(
        attempt,
        options.initial_delay_ms,
        options.max_delay_ms,
        options.jitter_fraction,
        options.backoff_multiplier,
    )


def poll_until_done(
    retrieve: Callable[[], T],
    is_terminal: Callable[[T], bool],
    options: Optional[PollingOptions] = None,
) -> T:
    """
    Polls a retrieve function until a terminal condition is met (synchronous version).

    Uses a hybrid polling strategy: fast polling at fixed intervals for an initial
    period, then exponential backoff with proportional jitter. This provides low
    latency for quick operations while still reducing server load for longer ones.

    Default behavior:
    - Fast phase: Poll every 1 second for the first 30 seconds
    - Backoff phase: Exponential backoff with 1.15x multiplier, max 30 second delay

    Args:
        retrieve: Function that fetches the current state
        is_terminal: Predicate that returns True when polling should stop
        options: Polling configuration options

    Returns:
        The final result when is_terminal returns True

    Raises:
        PollingTimeoutError: If max_wait_ms is set and exceeded

    Example:
        # Default hybrid polling
        result = poll_until_done(
            retrieve=lambda: client.extract_runs.retrieve(run_id),
            is_terminal=lambda res: res.extract_run.status != "PROCESSING"
        )

        # Pure exponential backoff (disable fast polling phase)
        result = poll_until_done(
            retrieve=lambda: client.extract_runs.retrieve(run_id),
            is_terminal=lambda res: res.extract_run.status != "PROCESSING",
            options=PollingOptions(fast_poll_duration_ms=0)
        )
    """
    if options is None:
        options = PollingOptions()

    max_wait_ms = options.max_wait_ms
    hybrid_options = HybridDelayOptions(
        fast_poll_duration_ms=options.fast_poll_duration_ms,
        fast_poll_interval_ms=options.fast_poll_interval_ms,
        initial_delay_ms=options.initial_delay_ms,
        max_delay_ms=options.max_delay_ms,
        backoff_multiplier=options.backoff_multiplier,
        jitter_fraction=options.jitter_fraction,
    )

    start_time = time.time() * 1000  # Convert to milliseconds

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

        delay = calculate_hybrid_delay(elapsed_ms, hybrid_options)

        # If timeout is set, don't wait longer than remaining time
        if max_wait_ms is not None:
            remaining_ms = max_wait_ms - elapsed_ms
            actual_delay = min(delay, remaining_ms)
        else:
            actual_delay = delay

        time.sleep(actual_delay / 1000)  # Convert to seconds for time.sleep


async def poll_until_done_async(
    retrieve: Callable[[], Awaitable[T]],
    is_terminal: Callable[[T], bool],
    options: Optional[PollingOptions] = None,
) -> T:
    """
    Polls a retrieve function until a terminal condition is met (asynchronous version).

    Uses a hybrid polling strategy: fast polling at fixed intervals for an initial
    period, then exponential backoff with proportional jitter. This provides low
    latency for quick operations while still reducing server load for longer ones.

    Default behavior:
    - Fast phase: Poll every 1 second for the first 30 seconds
    - Backoff phase: Exponential backoff with 1.15x multiplier, max 30 second delay

    Args:
        retrieve: Async function that fetches the current state
        is_terminal: Predicate that returns True when polling should stop
        options: Polling configuration options

    Returns:
        The final result when is_terminal returns True

    Raises:
        PollingTimeoutError: If max_wait_ms is set and exceeded

    Example:
        # Default hybrid polling
        result = await poll_until_done_async(
            retrieve=lambda: client.extract_runs.retrieve(run_id),
            is_terminal=lambda res: res.extract_run.status != "PROCESSING"
        )

        # Pure exponential backoff (disable fast polling phase)
        result = await poll_until_done_async(
            retrieve=lambda: client.extract_runs.retrieve(run_id),
            is_terminal=lambda res: res.extract_run.status != "PROCESSING",
            options=PollingOptions(fast_poll_duration_ms=0)
        )
    """
    if options is None:
        options = PollingOptions()

    max_wait_ms = options.max_wait_ms
    hybrid_options = HybridDelayOptions(
        fast_poll_duration_ms=options.fast_poll_duration_ms,
        fast_poll_interval_ms=options.fast_poll_interval_ms,
        initial_delay_ms=options.initial_delay_ms,
        max_delay_ms=options.max_delay_ms,
        backoff_multiplier=options.backoff_multiplier,
        jitter_fraction=options.jitter_fraction,
    )

    start_time = time.time() * 1000  # Convert to milliseconds

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

        delay = calculate_hybrid_delay(elapsed_ms, hybrid_options)

        # If timeout is set, don't wait longer than remaining time
        if max_wait_ms is not None:
            remaining_ms = max_wait_ms - elapsed_ms
            actual_delay = min(delay, remaining_ms)
        else:
            actual_delay = delay

        await asyncio.sleep(actual_delay / 1000)  # Convert to seconds for asyncio.sleep
