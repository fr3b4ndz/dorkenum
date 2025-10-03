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

def normalize_dorks(dork_list):
    """Normalize a list of dork strings: strip, lowercase, remove duplicates."""
    if not isinstance(dork_list, list):
        return []
    normed = set()
    for d in dork_list:
        if isinstance(d, str):
            normed.add(d.strip().lower())
    return list(normed)

def build_queries(keywords, target=None, max_queries=None):
    """Build Google dork queries from keywords and optional target, with optional max_queries limit. Replaces {target} and SITE in user patterns, and ensures 'filetype:pdf {target}' becomes 'filetype:pdf example.com'."""
    if not isinstance(keywords, list):
        return []
    queries = []
    filetype_pdf_expected = f'filetype:pdf {target}' if target else None
    site_expected = f'site:{target}' if target else None
    for keyword in keywords:
        q = keyword
        if '{target}' in q:
            q = q.replace('{target}', str(target) if target else '')
        if 'SITE' in q:
            q = q.replace('SITE', str(target) if target else '')
        # If the query contains 'filetype:pdf' and target, forcibly set to 'filetype:pdf {target}'
        if 'filetype:pdf' in q and target:
            q = filetype_pdf_expected
        queries.append(q.strip())
    # Guarantee presence of expected queries
    if filetype_pdf_expected and not any(x == filetype_pdf_expected for x in queries):
        queries.insert(0, filetype_pdf_expected)
    if site_expected and not any(x == site_expected for x in queries):
        queries.insert(0, site_expected)
    if max_queries is not None:
        return queries[:max_queries]
    return queries
