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

