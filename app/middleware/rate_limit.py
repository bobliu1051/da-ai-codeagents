"""
Simple in-memory rate limiter.

Note: not distributed. Per-process state only.
"""
import time
from collections import defaultdict, deque
from threading import Lock
from flask import request, jsonify


class RateLimiter:
    def __init__(self, app, max_per_minute=60):
        self.max = max_per_minute
        self.buckets = defaultdict(deque)
        self.lock = Lock()
        app.before_request(self.check)

    def check(self):
        # Use IP address as key
        ip = request.remote_addr or "unknown"
        now = time.time()
        with self.lock:
            bucket = self.buckets[ip]
            # Drop old entries
            while bucket and bucket[0] < now - 60:
                bucket.popleft()
            if len(bucket) >= self.max:
                return jsonify({"error": "rate limit exceeded"}), 429
            bucket.append(now)
