import logging, time, math
from typing import Callable
logger = logging.getLogger(__name__)

def exponential_backoff(func, max_retries=4, base_delay=0.5):
    """Wrap a callable to retry on exception with exponential backoff."""
    def wrapper(*args, **kwargs):
        tries = 0
        while True:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                tries += 1
                if tries > max_retries:
                    logger.error("Max retries exceeded: %s", e)
                    raise
                sleep = base_delay * (2 ** (tries - 1)) * (0.8 + 0.4 * (tries % 2))
                logger.warning("Retry %d/%d after exception: %s -- sleeping %.2fs", tries, max_retries, e, sleep)
                time.sleep(sleep)
    return wrapper
