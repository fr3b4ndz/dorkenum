import os, json, csv, logging, time
from typing import List
from pathlib import Path
import requests, yaml
from jinja2 import Environment, select_autoescape

from .utils import exponential_backoff
logger = logging.getLogger(__name__)

def fetch_gist_lines(gist_url: str) -> List[str]:
    raw_url = gist_url
    if "gist.github.com" in gist_url and "/raw" not in gist_url:
        raw_url = gist_url.rstrip("/") + "/raw"
    logger.debug("Fetching gist from %s", raw_url)
    r = requests.get(raw_url, timeout=15)
    r.raise_for_status()
    lines = [ln.strip() for ln in r.text.splitlines()]
    return lines

def save_queries(queries: List[str], outpath: str):
    Path(outpath).parent.mkdir(parents=True, exist_ok=True)
    with open(outpath, "w", encoding="utf-8") as f:
        for q in queries:
            f.write(q + "\n")

def export_results(aggregated: List[dict], outpath: str, fmt: str = "json"):
    Path(outpath).parent.mkdir(parents=True, exist_ok=True)
    fmt = fmt.lower()
    if fmt == "json":
        with open(outpath, "w", encoding="utf-8") as f:
            json.dump(aggregated, f, indent=2)
    elif fmt == "csv":
        rows = []
        for item in aggregated:
            q = item.get("query")
            engine = item.get("engine")
            response = item.get("response", {})
            if isinstance(response, dict):
                results = response.get("webPages", {}).get("value", [])
                for r in results:
                    rows.append({
                        "query": q,
                        "engine": engine,
                        "title": r.get("name"),
                        "url": r.get("url"),
                        "snippet": r.get("snippet")
                    })
        keys = ["query", "engine", "title", "url", "snippet"]
        with open(outpath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(rows)
    elif fmt == "html":
        env = Environment(autoescape=select_autoescape(['html','xml']))
        tpl = env.from_string("""
        <!doctype html>
        <html lang=\"en\">
        <head>
          <meta charset=\"utf-8\">
          <meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
          <title>dorkenum results</title>
          <style>
            body{font-family: system-ui, -apple-system,Segoe UI,Roboto,Helvetica,Arial;line-height:1.4;padding:20px;}
            .query{margin-top:24px;padding:12px;border-radius:8px;background:#f7f7f9;}
            .meta{font-size:0.9rem;color:#555;}
            ul{margin:6px 0 16px 20px;}
            li{margin-bottom:8px;}
            .snippet{color:#333;font-size:0.95rem;}
            .title{font-weight:600;}
            .summary{background:#eef;padding:10px;border-radius:6px;}
          </style>
        </head>
        <body>
          <h1>dorkenum results</h1>
          <div class=\"summary\">Generated {{ aggregated|length }} query result groups.</div>
          {% for item in aggregated %}
            <div class=\"query\">
              <div class=\"meta\"><strong>Query:</strong> {{ item.query }} — <em>{{ item.engine }}</em></div>
              {% set hits = (item.response.webPages.value if item.response is mapping and item.response.get('webPages') else []) %}
              {% if hits %}
                <ul>
                {% for r in hits %}
                  <li>
                    <div class=\"title\"><a href=\"{{ r.url }}\" target=\"_blank\" rel=\"noopener noreferrer\">{{ r.name }}</a></div>
                    <div class=\"snippet\">{{ r.snippet }}</div>
                  </li>
                {% endfor %}
                </ul>
              {% else %}
                <div class=\"meta\">No hits found for this query.</div>
              {% endif %}
            </div>
          {% endfor %}
        </body>
        </html>
        """)
        safe_agg = []
        for it in aggregated:
            resp = it.get('response') or {}
            if not isinstance(resp, dict):
                resp = {}
            safe_agg.append({'query': it.get('query'), 'engine': it.get('engine'), 'response': resp})
        rendered = tpl.render(aggregated=safe_agg)
        with open(outpath, "w", encoding="utf-8") as f:
            f.write(rendered)
    else:
        raise ValueError("Unsupported format: %s" % fmt)

def load_config(path: str = None):
    if not path:
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
