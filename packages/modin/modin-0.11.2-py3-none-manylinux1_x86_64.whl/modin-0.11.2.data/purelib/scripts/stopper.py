import time
import sys
import functools

class TooSlow(Exception):
    pass

class Timeout:
    def __init__(self, wait=5, callback=None):
        self.wait = wait
        self.stop = None
        self.oldprofile = None
        self.callback = callback
    def __enter__(self):
        self.stop = time.time() + self.wait
        self.oldprofile = sys.getprofile()
        sys.setprofile(self._checker)
        return self
    def __exit__(self, *a):
        self.stop = None
        sys.setprofile(self.oldprofile)
        return None
    def _checker(self, frame, event, arg):
        try:
            if self.stop is not None and time.time() >= self.stop:
                if not self.callback or self.callback(self):
                    raise TooSlow()
        finally:
            if self.oldprofile:
                self.oldprofile(frame, event, arg)

def timeout(wait=5):
    def wrapper(func):
        @functools.wraps(func)
        def wrapped(*a, **kw):
            with Timeout(wait=wait):
                return func(*a, **kw)
        return wrapped
    return wrapper

class Guardian:
    def __init__(self, wait=5):
        self.oldprofile = sys.getprofile()
        self.timers = {}
        self.wait = wait
        sys.setprofile(self._checker)

    def _checker(self, frame, event, arg):
        if frame.f_code.co_name.startswith('test_'):
            if event == 'call':
                def timed_out(timer, guard=self, frame=frame):
                    guard.disable_timer(frame)
                    return True
                self.enable_timer(frame, callback=timed_out)
            elif event == 'return':
                self.disable_timer(frame)
        if self.oldprofile:
            self.oldprofile(frame, event, arg)

    def enable_timer(self, frame, callback=None):
        self.timers[frame] = Timeout(wait=self.wait, callback=callback).__enter__()
        print(f'enabled timeout for {frame.f_code.co_name}')

    def disable_timer(self, frame):
        timer = self.timers.pop(frame, None)
        if timer:
            timer.__exit__()
        print(f'disabled timeout for {frame.f_code.co_name}')

@timeout(3)
def slow(n):
    for _ in range(n):
        time.sleep(1.0)

def test_slow(n=7):
    for _ in range(n):
        time.sleep(1.0)

def test_fast():
    time.sleep(0.5)

if __name__ == '__main__':
    Guardian(3)
    test_fast()
    test_slow(5)
    slow(10)
