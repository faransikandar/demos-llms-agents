import time
from functools import wraps

def benchmark(func):
    @wraps(func)  # <== ✅ This preserves type annotations for FastAPI
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = round(time.time() - start, 4)
        print(f"[⏱] {func.__name__} took {duration}s")
        return result
    return wrapper
