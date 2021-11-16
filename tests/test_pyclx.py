import numpy as np
from pathlib import Path
import pyclx.pyclx as px
import pytest

TEST_ROOT = Path(__file__).parent
clx_dir = str(TEST_ROOT / 'resources')

pars_read_celex = [
    (None, False, None, (100,7), np.int64),
    (None, False, 'Word', (100,6), object),
    (['Word'], False, None, (100,1), np.int64),
    (['Word'], True, None, (100,), np.int64)
]
@pytest.mark.parametrize('usecols, squeeze, index_col, shape, indtype', pars_read_celex)
def test_read_celex (usecols, squeeze, index_col, shape, indtype):
    clx = px.read_celex('gpw', clx_dir, usecols, squeeze, index_col)
    assert clx.shape==shape
    assert clx.index.dtype==indtype

