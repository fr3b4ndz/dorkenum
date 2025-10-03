

import click
import os
from .utils import build_queries
from .api import run_google_search, run_shodan_search, run_google_search_paginated
from .core import export_results

# API keys (use placeholders for GitHub)
GOOGLE_API_KEY = "<GOOGLE_API_KEY>"
GOOGLE_CSE_ID = "<GOOGLE_CSE_ID>"
SHODAN_API_KEY = "<SHODAN_API_KEY>"

@click.group()
def cli():
    """Dorkenum CLI group."""
    pass



@cli.command()
@click.option('--target', required=True, help='Target domain or IP')
@click.option('--api', type=click.Choice(['google', 'shodan'], case_sensitive=False), default='google', help='API to use')
@click.option('--google-dork', multiple=True, help='Google dorks using supported filters: site, inurl, intitle, filetype, ext, intext, etc. Example: "site:oklahoma.gov inurl:login filetype:pdf"')
@click.option('--shodan-dork', multiple=True, help='Shodan queries using supported filters: product, port, org, country, city, region, hostname, os, etc. Example: "product:\"Siemens\" country:\"US\" port:502"')
@click.option('--out', default='results.json', help='Output file')
@click.option('--format', type=click.Choice(['json', 'txt'], case_sensitive=False), default='json', help='Output format')
@click.option('--yes', is_flag=True, help='Overwrite output file if exists')
def run(target, api, google_dork, shodan_dork, out, format, max_results=None, page_size=None, yes=False):
    """Run queries and save results."""
    queries = build_queries(target, list(google_dork))
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
            while True:
                resp = run_shodan_search(query, SHODAN_API_KEY, page=page, minify=False)
                matches = resp.get('matches', [])
                all_results.extend(matches)
                if not matches or len(matches) < 100:
                    break
                page += 1
                if max_results is not None and len(all_results) >= int(max_results):
                    break
            if max_results is not None:
                resp['matches'] = all_results[:int(max_results)]
            else:
                resp['matches'] = all_results
            results.append({'query': query, 'raw_response': resp})
    if os.path.exists(out) and not yes:
        click.confirm(f"{out} exists. Overwrite?", abort=True)
    export_results(results, out, format)
    click.echo(f"Results written to {out}")

if __name__ == "__main__":
    cli()

if __name__ == "__main__":
    cli()
