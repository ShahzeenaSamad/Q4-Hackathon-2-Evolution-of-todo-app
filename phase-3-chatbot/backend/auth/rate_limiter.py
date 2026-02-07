"""
Rate Limiter Module - 5 attempts per 15 min per IP
"""
from datetime import datetime, timedelta
from collections import defaultdict


class RateLimiter:
    """In-memory rate limiter with local storage"""
    def __init__(self, max_attempts: int = 5, window_minutes: int = 15):
        self.max_attempts = max_attempts
        self.window_minutes = window_minutes
        self.attempts: dict = defaultdict(list)
        self.last_cleanup = datetime.now()

    def _cleanup_old_entries(self):
        """Remove attempts older than window"""
        cutoff_time = datetime.now() - timedelta(minutes=self.window_minutes)
        for ip_address in list(self.attempts.keys()):
            self.attempts[ip_address] = [
                t for t in self.attempts[ip_address]
                if t > cutoff_time
            ]
            if not self.attempts[ip_address]:
                del self.attempts[ip_address]
        self.last_cleanup = datetime.now()

    def is_rate_limited(self, ip_address: str) -> bool:
        """Check if IP exceeded rate limit (5 attempts / 15 min)"""
        if self._cleanup_needed():
            self._cleanup_old_entries()
        attempts = self.attempts.get(ip_address, [])
        cutoff_time = datetime.now() - timedelta(minutes=self.window_minutes)
        recent_attempts = [t for t in attempts if t > cutoff_time]
        if len(recent_attempts) >= self.max_attempts:
            return True
        self.attempts[ip_address] = recent_attempts + [datetime.now()]
        return False

    def _cleanup_needed(self) -> bool:
        """Check if cleanup is needed (every hour)"""
        return datetime.now() - self.last_cleanup > timedelta(hours=1)

    def reset_attempts(self, ip_address: str):
        """Reset rate limit for successful login"""
        if ip_address in self.attempts:
            del self.attempts[ip_address]


# Global rate limiter instance
_rate_limiter = RateLimiter(max_attempts=5, window_minutes=15)


def get_rate_limit_status(ip_address: str) -> tuple:
    """Get rate limit status (is_limited, attempts, max_attempts)"""
    return (
        _rate_limiter.is_rate_limited(ip_address),
        len(_rate_limiter.attempts.get(ip_address, [])),
        _rate_limiter.max_attempts
    )
