# example of group by/flattening operations
import pandas as pd
from pandas_examples.aux import manual_agg_func


df = pd.DataFrame.from_dict({'id':[1, 1, 1, 2, 2, 2],
                             'old':['a', 'b', 'c', 'd', 'e', 'f'],
                             'marker':[1, 2, 3, 1, 2, 3]})


# basic groupby  - how to get at sensible data slices
df_grp = df.groupby("id").agg({'marker':['count', 'min', 'max'],
                               'old':'count'})

df_grp_ri = df_grp.reset_index() # doesn't flatten
# solution: renaming columns
dfg_cp = df_grp.copy()
dfg_cp.columns = [('_'.join(col).strip()).rstrip('_') for col in dfg_cp.columns.values]
dfg_cp = dfg_cp.reset_index()


# df_grp: lvl0: marker
# df_grp lvl1: count mean max min

idx = pd.IndexSlice
dftmp = df_grp.loc[idx[:], idx[:, "max"]]
dftmp = df_grp.loc[idx[:], idx["marker", "max"]]

dftmp = df_grp.loc[idx[:], idx[:, "count"]]

# this method doesn't require reset inde
dfi_F = df.groupby("id", as_index=False).apply(manual_agg_func)

dfi_T = df.groupby("id", as_index=True).apply(manual_agg_func).reset_index()


                            
