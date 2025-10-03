from dorkenum.utils import exponential_backoff, normalize_dorks, build_queries
import time
def test_exponential_backoff_wrapper():
    calls = {'n':0}
    def flaky(a):
        calls['n'] += 1
        if calls['n'] < 3:
            raise ValueError('fail')
        return 'ok'
    wrapped = exponential_backoff(flaky, max_retries=4, base_delay=0.01)
    assert wrapped(1) == 'ok'
def test_normalize_dorks_minimal():
    lines = [
        "site:example.com inurl:admin",
        "not a dork line",
        "inurl:login site:TARGET",
        "# comment line",
    ]
    out = normalize_dorks(lines)
    assert any("inurl:admin" in x for x in out)
    assert any("inurl:login" in x for x in out)
def test_build_queries_replacement():
    dorks = ["inurl:login SITE", "filetype:pdf {target}"]
    q = build_queries(dorks, "example.com", max_queries=10)
    assert any("site:example.com" in x for x in q)
    assert any("filetype:pdf example.com" in x for x in q)
