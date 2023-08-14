from pathlib import Path
import pyclx.pyclx as px
import pandas as pd
import pytest

TEST_ROOT = Path(__file__).parent
clx_dir = str(TEST_ROOT / 'resources')

pars_read_celex = [
    (None,           False, None, (51728, 50),  8),
    (None,           False,   10, (   10, 20), 13),
    (None,            True, None, (51728, 50),  8),
    (None,            True,   10, (   10, 20), 13),
    (['Head','Def'], False, None, (51728,  4),  4),
    (['Head','Def'], False,   10, (   10,  2),  2),
    (['Head','Def'],  True, None, (51728,  4),  4),
    (['Head','Def'],  True,   10, (   10,  2),  2),
    (['Head'],       False, None, (51728,  1),  1),
    (['Head'],       False,   10, (   10,  1),  1),
    (['Head'],        True, None, (51728,   ),  0),
    (['Head'],        True,   10, (   10,   ),  0)
]

@pytest.mark.parametrize('usecols, squeeze, nrows, shape, unqclm', pars_read_celex)
def test_read_celex (usecols, squeeze, nrows, shape, unqclm):
    clx = px.read_celex('gml', clx_dir, usecols, squeeze, nrows)
    assert clx.shape==shape
    if isinstance(clx, pd.core.series.Series):
        _unqclm = 0
    else:
        _unqclm = len(set(pd.Series(clx.columns).apply(lambda x: x[-1])))
    assert _unqclm==unqclm



