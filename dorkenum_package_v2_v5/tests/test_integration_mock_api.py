import json
from dorkenum.core import export_results
SAMPLE_BING_RESPONSE = {
    "webPages": {
        "value": [
            {"name": "Example - Admin", "url": "https://example.com/admin", "snippet": "Admin panel"},
            {"name": "Example - Login", "url": "https://example.com/login", "snippet": "Login page"}
        ]
    }
}
def test_export_csv_and_html(tmp_path):
    agg = [{"query": "inurl:admin site:example.com", "engine": "bing", "response": SAMPLE_BING_RESPONSE}]
    out_csv = tmp_path / "out.csv"
    out_html = tmp_path / "out.html"
    export_results(agg, str(out_csv), fmt="csv")
    export_results(agg, str(out_html), fmt="html")
    txt = out_csv.read_text(encoding='utf-8')
    assert "example.com/admin" in txt or "https://example.com/admin" in txt
    h = out_html.read_text(encoding='utf-8')
    assert "Example - Admin" in h
