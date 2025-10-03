# dorkenum

Improved `dorkenum` — a safe Google-dork query generator and optional official-search-API runner.

**Key features:**
- Generates focused dork queries from template sources (gists, files).
- Optional execution using official search APIs (Bing or Google) with environment-gated keys.
- Safe-by-default: generation-only unless explicitly asked to run.
- Logging, retries with exponential backoff, CSV/JSON/HTML export, YAML config support.
- Tests (pytest) and GitHub Actions CI workflow included.

## Quick start

1. Clone repository and create virtualenv:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Generate queries (safe default):

```bash
python -m dorkenum.cli generate --target example.com --gist-url https://gist.github.com/sundowndev/283efaddbcf896ab405488330d1bbc06 --out queries.txt
```

3. Run queries with Bing (requires env `BING_API_KEY`):

```bash
export BING_API_KEY=your_key_here
python -m dorkenum.cli run --target example.com --api bing --limit 10 --results 5 --yes --out results.json --format csv
```

4. Run tests:

```bash
pytest -q
```

## Ethics & Authorization

See `ETHICS.md` for usage rules and an explicit authorization checklist. Always obtain written authorization before running enumeration against third-party targets.
