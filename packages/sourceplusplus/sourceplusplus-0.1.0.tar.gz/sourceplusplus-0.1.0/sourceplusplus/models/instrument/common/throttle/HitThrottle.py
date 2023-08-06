import time

from .ThrottleStep import ThrottleStep


class HitThrottle:
    def __init__(self, limit: int, step: ThrottleStep):
        self.limit = limit
        self.step = step
        self.last_reset = -1
        self.hit_count = 0
        self.total_hit_count = 0
        self.total_limited_count = 0

    def is_rate_limited(self) -> bool:
        if self.hit_count < self.limit:
            self.hit_count += 1
            self.total_hit_count += 1
            return False
        self.hit_count += 1

        if round(time.time() * 1000) - self.last_reset > self.step.get_millis(1):
            self.hit_count = 1
            self.total_hit_count += 1
            self.last_reset = round(time.time() * 1000)
            return False
        else:
            self.total_limited_count += 1
            return True

    def get_total_hit_count(self):
        return self.total_hit_count

    def get_total_limited_count(self):
        return self.total_limited_count
