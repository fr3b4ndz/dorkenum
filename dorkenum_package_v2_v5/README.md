### 7. Enumerate Vendor Sites for Default Logins

Identify vendor portals and devices that may use default credentials. Useful for assessing exposure of network equipment, web applications, and IoT devices.

#### Example: Cisco Device Default Logins
```bash
python -m dorkenum.cli generate --target cisco.com --dorks "intitle:login inurl:cgi-bin site:{target}" "inurl:level/15/exec/-/ site:{target}" --out cisco_default_logins.txt
```

#### Example: WordPress Admin Default Logins
```bash
python -m dorkenum.cli generate --target vendor-site.com --dorks "inurl:wp-admin site:{target}" "intitle:WordPress inurl:login site:{target}" --out wp_default_logins.txt
```

#### Example: IoT Device Default Logins (Generic)
```bash
python -m dorkenum.cli generate --target vendor-site.com --dorks "intitle:login inurl:admin site:{target}" "inurl:setup.cgi site:{target}" --out iot_default_logins.txt
```

#### Example: Export and Search for Default Credentials
```bash
export BING_API_KEY=your_key_here
python -m dorkenum.cli run --target vendor-site.com --api bing --dorks "intitle:login site:{target}" --out default_login_results.json --format json
```
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


## Practical OSINT Usage Examples for Security Professionals

### 1. Reconnaissance: Enumerate Public Resources for a Target

Generate dork queries to discover public resources related to a target domain:

```bash
python -m dorkenum.cli generate --target acme-corp.com --gist-url https://gist.github.com/sundowndev/283efaddbcf896ab405488330d1bbc06 --out acme_queries.txt
```

### 2. Discover Exposed Documents (e.g., PDFs)

Find potentially sensitive documents exposed on a target domain:

```bash
python -m dorkenum.cli generate --target acme-corp.com --dorks "filetype:pdf {target}" --out pdf_queries.txt
```

### 3. Enumerate Login Portals and Admin Pages

Identify login pages and admin portals for a target:

```bash
python -m dorkenum.cli generate --target acme-corp.com --dorks "inurl:login SITE" "inurl:admin SITE" --out portals.txt
```

### 4. Automated Search and Export for Reporting

Run dork queries using Bing API and export results for reporting:

```bash
export BING_API_KEY=your_key_here
python -m dorkenum.cli run --target acme-corp.com --api bing --limit 20 --results 10 --yes --out acme_results.json --format csv
```

### 5. Use a Custom Dork List File

Leverage your own curated dork list for targeted enumeration:

```bash
python -m dorkenum.cli generate --target acme-corp.com --dork-file my_dorks.txt --out custom_queries.txt
```

### 6. Export Results in Multiple Formats

Export search results to CSV, JSON, or HTML for further analysis or reporting:

```bash
python -m dorkenum.cli run --target acme-corp.com --api bing --out results.csv --format csv
python -m dorkenum.cli run --target acme-corp.com --api bing --out results.html --format html
```

---

See `ETHICS.md` for usage rules and an explicit authorization checklist. Always obtain written authorization before running enumeration against third-party targets.
