from dorkenum.core import export_results
def fake_bing_get_response(offset, count):
    results = []
    for i in range(offset, offset+count):
        results.append({'name': f'Hit {i}', 'url': f'https://example.com/page{i}', 'snippet': f'Snippet {i}'})
    return {'webPages': {'value': results}}
def test_pagination_csv_and_html(tmp_path):
    resp1 = fake_bing_get_response(0,3)
    resp2 = fake_bing_get_response(3,3)
    agg = []
    agg.append({'query':'inurl:admin site:example.com','engine':'bing','response': resp1})
    agg.append({'query':'inurl:admin site:example.com','engine':'bing','response': resp2})
    out_csv = tmp_path / 'pag.csv'
    out_html = tmp_path / 'pag.html'
    export_results(agg, str(out_csv), fmt='csv')
    export_results(agg, str(out_html), fmt='html')
    csv_text = out_csv.read_text(encoding='utf-8')
    assert 'https://example.com/page0' in csv_text
    assert 'https://example.com/page3' in csv_text
    html_text = out_html.read_text(encoding='utf-8')
    assert 'Hit 0' in html_text and 'Hit 3' in html_text
