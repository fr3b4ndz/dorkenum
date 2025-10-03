

import click
import os
from .utils import build_queries
from .api import run_google_search, run_shodan_search, run_google_search_paginated
from .core import export_results

# Hardcoded API keys (replace with your own keys)
GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"
GOOGLE_CSE_ID = "YOUR_GOOGLE_CSE_ID"
SHODAN_API_KEY = "YOUR_SHODAN_API_KEY"

@click.group()
def cli():
    """Dorkenum CLI group."""
    pass

@cli.command()
@click.option('--target', required=True, help='Target domain or IP')
@click.option('--dorks', multiple=True, help='Google dorks using supported filters: site, inurl, intitle, filetype, ext, intext, cache, link, related, info, define, stocks, map, weather, source, allinurl, allintitle, allintext, allinanchor, etc. Example: "site:oklahoma.gov inurl:login filetype:pdf"')
@click.option('--shodan-dork', multiple=True, help='Shodan queries using supported filters: product, port, org, country, city, region, hostname, os, version, isp, asn, domain, vulns, ssl, device, before, after, geo, net, etc. Example: "product:\"Siemens\" country:\"US\" port:502"')
@click.option('--api', type=click.Choice(['google', 'shodan'], case_sensitive=False), default='google', help='API to use')
@click.option('--out', default='results.json', help='Output file')
@click.option('--format', type=click.Choice(['json', 'txt'], case_sensitive=False), default='json', help='Output format')
@click.option('--max-results', default=50, show_default=True, help='Maximum results to enumerate per query (pagination)')
@click.option('--page-size', default=10, show_default=True, help='Results per page (Google only)')
@click.option('--yes', is_flag=True, help='Overwrite output file if exists')
def generate(target, dorks, shodan_dork, api, out, format, max_results, page_size, yes):
    """Generate dorks and run queries."""
    queries = build_queries(target, list(dorks))
    if shodan_dork:
        queries.extend(list(shodan_dork))
    results = []
    if api == 'google':
        for query in queries:
            res = run_google_search_paginated(query, GOOGLE_API_KEY, GOOGLE_CSE_ID, max_results=max_results, page_size=page_size)
            results.append({'query': query, 'raw_response': res})
    elif api == 'shodan':
        for query in queries:
            all_results = []
            page = 1
            while len(all_results) < max_results:
                resp = run_shodan_search(query, SHODAN_API_KEY, page=page, minify=False)
                matches = resp.get('matches', [])
                all_results.extend(matches)
                if not matches or len(matches) < 100:
                    break
                page += 1
            resp['matches'] = all_results[:max_results]
            results.append({'query': query, 'raw_response': resp})
    if os.path.exists(out) and not yes:
        click.confirm(f"{out} exists. Overwrite?", abort=True)
    export_results(results, out, format)
    click.echo(f"Results written to {out}")

@cli.command()
@click.option('--target', required=True, help='Target domain or IP')
@click.option('--api', type=click.Choice(['google', 'shodan'], case_sensitive=False), default='google', help='API to use')
@click.option('--dorks', multiple=True, help='Google dorks using supported filters: site, inurl, intitle, filetype, ext, intext, etc. Example: "site:oklahoma.gov inurl:login filetype:pdf"')
@click.option('--shodan-dork', multiple=True, help='Shodan queries using supported filters: product, port, org, country, city, region, hostname, os, etc. Example: "product:\"Siemens\" country:\"US\" port:502"')
@click.option('--out', default='results.json', help='Output file')
@click.option('--format', type=click.Choice(['json', 'txt'], case_sensitive=False), default='json', help='Output format')
@click.option('--yes', is_flag=True, help='Overwrite output file if exists')
def run(target, api, dorks, shodan_dork, out, format, max_results, page_size, yes):
    """Run queries and save results."""
    queries = build_queries(target, list(dorks))
    if shodan_dork:
        queries.extend(list(shodan_dork))
    results = []
    if api == 'google':
        for query in queries:
            res = run_google_search_paginated(query, GOOGLE_API_KEY, GOOGLE_CSE_ID, max_results=max_results, page_size=page_size)
            results.append({'query': query, 'raw_response': res})
    elif api == 'shodan':
        for query in queries:
            all_results = []
            page = 1
            while len(all_results) < max_results:
                resp = run_shodan_search(query, SHODAN_API_KEY, page=page, minify=False)
                matches = resp.get('matches', [])
                all_results.extend(matches)
                if not matches or len(matches) < 100:
                    break
                page += 1
            resp['matches'] = all_results[:max_results]
            results.append({'query': query, 'raw_response': resp})
    if os.path.exists(out) and not yes:
        click.confirm(f"{out} exists. Overwrite?", abort=True)
    export_results(results, out, format)
    click.echo(f"Results written to {out}")

if __name__ == "__main__":
    cli()

if __name__ == "__main__":
    cli()
