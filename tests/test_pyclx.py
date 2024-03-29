from pathlib import Path
import pyclx.pyclx as px
import pandas as pd
import numpy as np
import pytest

TEST_ROOT = Path(__file__).parent
clx_dir = str(TEST_ROOT / 'resources')


pars_read_celex = [
    ('gml', None,                   False, None, (10000, 50),  8),
    ('gml', None,                   False,   10, (   10, 20), 13),
    ('gml', None,                    True, None, (10000, 50),  8),
    ('gml', None,                    True,   10, (   10, 20), 13),
    ('gml', ['IdNum','Head','Def'], False, None, (10000,  5),  5),
    ('gml', ['IdNum','Head','Def'], False,   10, (   10,  3),  3),
    ('gml', ['IdNum','Head','Def'],  True, None, (10000,  5),  5),
    ('gml', ['IdNum','Head','Def'],  True,   10, (   10,  3),  3),
    ('gml', ['IdNum'],              False, None, (10000,  1),  1),
    ('gml', ['IdNum'],              False,   10, (   10,  1),  1),
    ('gml', ['IdNum'],               True, None, (10000,   ),  0),
    ('gml', ['IdNum'],               True,   10, (   10,   ),  0),
    ('dmw', None,                   False, None, (10000,  5),  5),
    ('dmw', None,                   False,   10, (   10,  5),  5),
    ('dmw', None,                    True, None, (10000,  5),  5),
    ('dmw', None,                    True,   10, (   10,  5),  5),
    ('dmw', ['Idnum','Word','Inl'], False, None, (10000,  3),  3),
    ('dmw', ['Idnum','Word','Inl'], False,   10, (   10,  3),  3),
    ('dmw', ['Idnum','Word','Inl'],  True, None, (10000,  3),  3),
    ('dmw', ['Idnum','Word','Inl'],  True,   10, (   10,  3),  3),
    ('dmw', ['Idnum'],              False, None, (10000,  1),  1),
    ('dmw', ['Idnum'],              False,   10, (   10,  1),  1),
    ('dmw', ['Idnum'],               True, None, (10000,   ),  0),
    ('dmw', ['Idnum'],               True,   10, (   10,   ),  0),
    ('epw', None,                   False, None, (10000, 97), 15),
    ('epw', None,                   False,   10, (   10, 21),  9),
    ('epw', None,                    True, None, (10000, 97), 15),
    ('epw', None,                    True,   10, (   10, 21),  9),
    ('epw', ['IdNum','Word','Cob'], False, None, (10000,  3),  3),
    ('epw', ['IdNum','Word','Cob'], False,   10, (   10,  3),  3),
    ('epw', ['IdNum','Word','Cob'],  True, None, (10000,  3),  3),
    ('epw', ['IdNum','Word','Cob'],  True,   10, (   10,  3),  3),
    ('epw', ['IdNum'],              False, None, (10000,  1),  1),
    ('epw', ['IdNum'],              False,   10, (   10,  1),  1),
    ('epw', ['IdNum'],               True, None, (10000,   ),  0),
    ('epw', ['IdNum'],               True,   10, (   10,   ),  0)
]

@pytest.mark.parametrize('which, usecols, squeeze, nrows, shape, unqclm', pars_read_celex)
def test_read_celex (which, usecols, squeeze, nrows, shape, unqclm):
    clx = px.read_celex(which, clx_dir, usecols, squeeze, nrows)
    assert clx.shape==shape
    if isinstance(clx, pd.core.series.Series):
        _unqclm = 0
        _isint  =  clx.dtypes==np.int64
    else:
        _unqclm = len(set(pd.Series(clx.columns).apply(lambda x: x[-1])))
        idnum   = 'IdNum' if 'IdNum' in clx.columns else 'Idnum'
        _isint  =  clx.dtypes[idnum]==np.int64
    assert _unqclm==unqclm
    assert _isint



