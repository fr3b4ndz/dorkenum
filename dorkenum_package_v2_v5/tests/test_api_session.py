from dorkenum.api import make_session, run_bing_search_paginated, run_google_search_paginated
def test_session_and_functions_exist():
    s = make_session()
    assert s is not None
    # functions exist and callable (do not call external APIs here)
    assert callable(run_bing_search_paginated)
    assert callable(run_google_search_paginated)
