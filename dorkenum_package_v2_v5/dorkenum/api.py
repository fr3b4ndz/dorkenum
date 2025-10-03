import requests
import time
from .utils import exponential_backoff

def make_session(timeout=15):
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(max_retries=3)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    # Wrap session.request with exponential backoff to handle transient errors
    session_request = session.request
    session.request = exponential_backoff(session_request)
    return session

# --- Bing Search (single-page) ---
def run_bing_search(query, api_key, count=10, offset=0):
    headers = {"Ocp-Apim-Subscription-Key": api_key}
    session = make_session()
    params = {"q": query, "count": count, "offset": offset}
    resp = session.get(
        "https://api.bing.microsoft.com/v7.0/search",
        headers=headers,
        params=params,
    )
    resp.raise_for_status()
    return resp.json()

# --- Bing Search (paginated) ---
def run_bing_search_paginated(query, api_key, max_results=50, page_size=10, delay=1.0):
    headers = {"Ocp-Apim-Subscription-Key": api_key}
    all_hits = []
    offset = 0
    session = make_session()
    while len(all_hits) < max_results:
        params = {"q": query, "count": page_size, "offset": offset}
        resp = session.get("https://api.bing.microsoft.com/v7.0/search", headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()
        values = data.get("webPages", {}).get("value", [])
        if not values:
            break
        for item in values:
            all_hits.append({
                "query": query,
                "engine": "bing",
                "title": item.get("name"),
                "url": item.get("url"),
                "snippet": item.get("snippet"),
            })
        offset += page_size
        time.sleep(delay)
    return all_hits[:max_results]

# --- Google Custom Search (single-page) ---
def run_google_search(query, api_key, cse_id, num=10, start=1):
    params = {"q": query, "key": api_key, "cx": cse_id, "num": num, "start": start}
    session = make_session()
    resp = session.get("https://www.googleapis.com/customsearch/v1", params=params)
    resp.raise_for_status()
    return resp.json()

# --- Google Custom Search (paginated) ---
def run_google_search_paginated(query, api_key, cse_id, max_results=50, page_size=10, delay=1.0):
    session = make_session()
    all_hits = []
    start = 1
    while len(all_hits) < max_results and start <= 91:
        num = min(page_size, 10)
        params = {"q": query, "key": api_key, "cx": cse_id, "start": start, "num": num}
        resp = session.get("https://www.googleapis.com/customsearch/v1", params=params)
        resp.raise_for_status()
        data = resp.json()
        items = data.get("items", [])
        if not items:
            break
        for item in items:
            all_hits.append({
                "query": query,
                "engine": "google",
                "title": item.get("title"),
                "url": item.get("link"),
                "snippet": item.get("snippet"),
            })
        start += num
        time.sleep(delay)
    return all_hits[:max_results]
