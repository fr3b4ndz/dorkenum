import os, sys, time, logging, click
from .core import fetch_gist_lines, save_queries, load_config, export_results
from .utils import normalize_dorks, build_queries
from .api import make_session, run_bing_search, run_bing_search_paginated, run_google_search, run_google_search_paginated

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("dorkenum")
DEFAULT_GIST = "https://gist.github.com/sundowndev/283efaddbcf896ab405488330d1bbc06"

@click.group()
def cli():
    pass

@cli.command()
@click.option("--target", required=True)
@click.option("--gist-url", default=DEFAULT_GIST)
@click.option("--out", default="queries.txt")
@click.option("--max", "max_q", default=500)
def generate(target, gist_url, out, max_q):
    click.echo("Fetching dork templates...")
    try:
        lines = fetch_gist_lines(gist_url)
    except Exception as e:
        click.echo(f"Error fetching gist: {e}", err=True)
        sys.exit(2)
    dorks = normalize_dorks(lines)
    queries = build_queries(dorks, target, max_queries=max_q)
    save_queries(queries, out)
    click.echo(f"Saved {len(queries)} queries to {out}")

@cli.command()
@click.option("--target", required=True)
@click.option("--api", type=click.Choice(["bing", "google"], case_sensitive=False), default="bing")
@click.option("--results", default=5)
@click.option("--limit", default=20)
@click.option("--delay", default=1.2)
@click.option("--gist-url", default=DEFAULT_GIST)
@click.option("--out", default="results.json")
@click.option("--format", "fmt", default="json", type=click.Choice(["json","csv","html"], case_sensitive=False))
@click.option("--config", default=None)
@click.option("--yes", is_flag=True)
def run(target, api, results, limit, delay, gist_url, out, fmt, config, yes):
    if not yes:
        click.confirm("Are you authorized to enumerate the target? (only proceed if yes)", abort=True)
    cfg = load_config(config) if config else {}
    lines = fetch_gist_lines(gist_url)
    dorks = normalize_dorks(lines)
    queries = build_queries(dorks, target, max_queries=limit)
    aggregated = []
    if api.lower() == "bing":
        bing_key = os.getenv("BING_API_KEY") or cfg.get("api", {}).get("bing_key")
        if not bing_key:
            click.echo("Missing BING_API_KEY env var or config.", err=True)
            sys.exit(3)
        for i, q in enumerate(queries, start=1):
            click.echo(f"[{i}/{len(queries)}] {q}")
            try:
                # use paginated fetch to gather up to `results` hits per query
                hits = run_bing_search_paginated(q, bing_key, max_results=results, page_size=min(10, results), delay=delay)
                aggregated.append({"query": q, "engine": "bing", "response": {"webPages": {"value": hits}}})
            except Exception as e:
                logger.error("API error: %s", e)
                continue
    else:
        google_key = os.getenv("GOOGLE_API_KEY") or cfg.get("api", {}).get("google_key")
        google_cx = os.getenv("GOOGLE_CSE_ID") or cfg.get("api", {}).get("google_cse_id")
        if not google_key or not google_cx:
            click.echo("Missing Google API key or CSE ID.", err=True)
            sys.exit(3)
        for i, q in enumerate(queries, start=1):
            click.echo(f"[{i}/{len(queries)}] {q}")
            try:
                hits = run_google_search_paginated(q, google_key, google_cx, max_results=results, page_size=min(10, results), delay=delay)
                aggregated.append({"query": q, "engine": "google", "response": {"webPages": {"value": hits}}})
            except Exception as e:
                logger.error("API error: %s", e)
                continue
    export_results(aggregated, out, fmt)
    click.echo(f"Exported results to {out} (format={fmt})")
