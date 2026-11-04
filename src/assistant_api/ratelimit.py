"""A tiny in-memory rate limiter (per client, per minute). Part F enforcement is mandatory for the team submission."""

from __future__ import annotations

import time
from collections import defaultdict, deque
from threading import Lock


class RateLimiter:
    def __init__(self, per_minute: int):
        self.per_minute = per_minute
        self._lock = Lock()
        self._hits: dict[str, deque[float]] = defaultdict(deque)

    def allow(self, key: str) -> bool:
        with self._lock:
            now = time.monotonic()
            q = self._hits[key]
            while q and now - q[0] > 60:
                q.popleft()
            if len(q) >= self.per_minute:
                return False
            q.append(now)
            return True
