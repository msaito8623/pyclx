import pandas as pd

def read_celex (which, clx_dir, usecols=None, squeeze=False, index_col=None):
    clx = '{}/{}.cd'.format(clx_dir,which)
    clx_rd = '{}/{}.readme'.format(clx_dir,which)
    with open(clx_rd, 'r') as f:
        clx_rd = f.readlines()
    clx_rd = [ i.strip() for i in clx_rd if i.strip()!='' ]
    
    aaa = pd.Series([ i[0].isdigit() for i in clx_rd ])
    first_digit_pos = aaa.index[aaa][0]
    non_digit_pos = aaa.index[~aaa]
    last_pos = non_digit_pos[non_digit_pos>first_digit_pos][0]
    clx_rd = clx_rd[first_digit_pos:last_pos]
    clx_rd = [ i.split() for i in clx_rd ]
    clms = [ i[1] for i in clx_rd ]
    clx = pd.read_csv(clx, sep='\\', header=None, names=clms, na_filter=False, usecols=usecols, squeeze=squeeze, index_col=index_col)
    return clx


