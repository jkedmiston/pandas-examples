"""#docgenstart
File output (pandas_examples/flattening.py): 
>>> df = pd.DataFrame.from_dict({'id':[1, 1, 1, 2, 2, 2],
                             'old':['a', 'b', 'c', 'd', 'e', 'f'],
                             'marker':[1, 2, 3, 1, 2, 3]})
>>> df
   id old  marker
0   1   a       1
1   1   b       2
2   1   c       3
3   2   d       1
4   2   e       2
5   2   f       3

>>> df_grp = df.groupby("id").agg({'marker':['count', 'min', 'max'],
                               'old':'count'})
>>> df_grp
   marker           old
    count min max count
id                     
1       3   1   3     3
2       3   1   3     3

>>> df_grp_ri = df_grp.reset_index() # doesn't flatten
>>> df_grp_ri
  id marker           old
      count min max count
0  1      3   1   3     3
1  2      3   1   3     3

>>> dfg_cp = df_grp.copy()
>>> dfg_cp
   marker           old
    count min max count
id                     
1       3   1   3     3
2       3   1   3     3

>>> dfg_cp.columns = [('_'.join(col).strip()).rstrip('_') for col in dfg_cp.columns.values]
>>> dfg_cp
    marker_count  marker_min  marker_max  old_count
id                                                 
1              3           1           3          3
2              3           1           3          3

>>> dfg_cp = dfg_cp.reset_index()
>>> dfg_cp
   id  marker_count  marker_min  marker_max  old_count
0   1             3           1           3          3
1   2             3           1           3          3

>>> idx = pd.IndexSlice
>>> idx
<pandas.core.indexing._IndexSlice object at 0x7fc9b902cdd8>

>>> dftmp = df_grp.loc[idx[:], idx[:, "max"]]
>>> dftmp
   marker
      max
id       
1       3
2       3

>>> dftmp = df_grp.loc[idx[:], idx["marker", "max"]]
>>> dftmp
id
1    3
2    3
Name: (marker, max), dtype: int64

>>> dftmp = df_grp.loc[idx[:], idx[:, "count"]]
>>> dftmp
   marker   old
    count count
id             
1       3     3
2       3     3

>>> dfi_F = df.groupby("id", as_index=False).apply(manual_agg_func)
>>> dfi_F
   marker_count  marker_max  marker_min  marker_mean
0           3.0         3.0         1.0          2.0
1           3.0         3.0         1.0          2.0

>>> dfi_T = df.groupby("id", as_index=True).apply(manual_agg_func).reset_index()
>>> dfi_T
   id  marker_count  marker_max  marker_min  marker_mean
0   1           3.0         3.0         1.0          2.0
1   2           3.0         3.0         1.0          2.0


#docgenend
"""

# example of group by/flattening operations
import pandas as pd

def manual_agg_func(dg):
    dg_cnt = dg["marker"].count()
    dg_max = dg["marker"].max()
    dg_min = dg["marker"].min()
    dg_mean = dg["marker"].mean()
    return pd.Series([dg_cnt, dg_max, dg_min, dg_mean], index=["marker_count",
                                                               "marker_max",
                                                               "marker_min",
                                                               "marker_mean"])



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


                            
# 
