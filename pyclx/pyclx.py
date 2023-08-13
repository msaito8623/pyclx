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
    cnames = find_colnames(readme_path, clen=clx.shape[1])
    clx.columns = cnames

    if not (usecols is None):
        colpos = pd.Series(clx.columns).str.replace('[0-9]$','',regex=True).isin(pd.Series(usecols))
        clx = clx.loc[:,colpos.to_list()]
    if all(pd.Series(clx.columns).apply(lambda x: x[-1])=='0'):
        clx.columns = pd.Series(clx.columns).apply(lambda x: x[:-1])
    if squeeze:
        clx = clx.squeeze('columns')
    return clx

def find_colnames (readme_path, clen=None):
    with open(readme_path, 'r') as f:
        rd = f.readlines()
    rd = pd.Series(rd).str.strip()
    rd = rd.loc[rd.str.contains('^[0-9]{1,2}\\. +[A-Za-z]+$', regex=True)].reset_index(drop=True)
    rd = rd.str.replace(' +', ' ', regex=True)
    rd = rd.str.split('. ', regex=False, expand=True).rename(columns={0:'ID',1:'Name'})
    assert ((rd.ID.astype(int) < rd.ID.astype(int).shift(-1)).iloc[:-1]).all()

    dup = rd.loc[rd.Name.duplicated(keep='first'),:].copy()
    dup['ID'] = range(rd.ID.astype(int).max()+1, rd.ID.astype(int).max()+len(dup)+1)
    rd = pd.concat([rd, dup], axis=0).reset_index(drop=True)

    d1 = rd.Name.duplicated(keep='first').astype(int)
    d2 = (rd.Name+rd.Name.duplicated(keep='first').astype(str)).duplicated(keep='first').astype(int)
    dup_ind = (d1 + d2).astype(str)
    rd['Name'] = rd.Name + dup_ind

    cnames = rd.Name.iloc[:clen]
    cnames.name = None
    return cnames


