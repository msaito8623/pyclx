import pandas as pd

def read_celex (which, clx_dir, usecols=None, squeeze=False, nrows=None):
    clx = '{}/{}.cd'.format(clx_dir, which)
    if nrows is None:
        with open(clx, 'r') as f:
            clx = f.readlines()
    else:
        with open(clx, 'r') as f:
            clx = [ next(f) for _ in range(nrows) ]
    clx = pd.Series(clx).str.strip()
    clx = clx.str.split('\\', regex=False, expand=True).fillna('')

    readme_path = '{}/{}.readme'.format(clx_dir, which)
    clx.columns = find_colnames(readme_path, clen=clx.shape[1])

    if not (usecols is None):
        colpos = pd.Series(clx.columns).str.replace('[0-9]$','',regex=True).isin(pd.Series(usecols))
        clx = clx.loc[:,colpos.to_list()]

    if set([ i[-1] for i in clx.columns if i[-1].isdigit() ])=={'0'}:
        clx.columns = pd.Series(clx.columns).str.replace('0$','',regex=True)
    if squeeze:
        clx = clx.squeeze('columns')
    clx = clx.apply(pd.to_numeric, errors='ignore')
    return clx

def find_colnames (readme_path, clen=None):
    with open(readme_path, 'r') as f:
        rd = f.readlines()
    rd = pd.Series(rd).str.strip()
    rd = rd.loc[rd.str.contains('^[0-9]{1,2}\\. +[A-Za-z]+$', regex=True)].reset_index(drop=True)
    rd = rd.str.replace(' +', ' ', regex=True)
    rd = rd.str.split('. ', regex=False, expand=True).rename(columns={0:'ID',1:'Name'})
    assert (( (rd.ID.astype(int)+1) == rd.ID.astype(int).shift(-1)).iloc[:-1]).all()
    rd = rd.Name

    hd = rd.loc[~rd.duplicated(keep=False)].copy().to_list()
    dp = rd.loc[ rd.duplicated(keep='last')].copy().to_list()
    assert clen%len(dp)==len(hd)

    dp = [dp]*(clen//len(dp))
    dp = [ [ j+str(ind) for j in i ] for ind,i in enumerate(dp) ]
    dp = [ j for i in dp for j in i ]
    rd = hd + dp
    assert clen==len(rd)
    return rd[:clen]


