"""#docgenstart
File output (pandas_examples/applying.py): 
>>> df = pd.DataFrame.from_dict({'id':[0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                             'age':[53.1, 54, 56, 54, 55, 56, 54, 55, 56, 54, 55, 55],
                             'marker':['group1', 'group1', 'group1', 'group2', 'group2', 'group2',
                                       'group1', 'group1', 'group1', 'group2', 'group2', 'group2'],
                             'value':[45, 48, 50, 51, 24, -10, 12, 14, 15, -1, -2, -3]})
>>> df
    id   age  marker  value
0    0  53.1  group1     45
1    2  54.0  group1     48
2    3  56.0  group1     50
3    4  54.0  group2     51
4    5  55.0  group2     24
5    6  56.0  group2    -10
6    7  54.0  group1     12
7    8  55.0  group1     14
8    9  56.0  group1     15
9   10  54.0  group2     -1
10  11  55.0  group2     -2
11  12  55.0  group2     -3

>>> df_mean = df.groupby("marker").mean()
>>> df_mean
              id        age      value
marker                                
group1  4.833333  54.683333  30.666667
group2  8.000000  54.833333   9.833333

>>> df_agg_mean = df.groupby("marker").agg('mean')
>>> df_agg_mean
              id        age      value
marker                                
group1  4.833333  54.683333  30.666667
group2  8.000000  54.833333   9.833333

>>> df_apply_mean = df.groupby("marker").apply(np.mean)
>>> df_apply_mean
              id        age      value
marker                                
group1  4.833333  54.683333  30.666667
group2  8.000000  54.833333   9.833333

>>> df_single = df.groupby("marker").apply(ret_single_value_basic)
>>> df_single
marker
group1    1.2
group2    1.2
dtype: float64

>>> df_series = df.groupby("marker").apply(ret_constant_series_basic)
>>> df_series
        val1  val2
marker            
group1   1.2   1.3
group2   1.2   1.3

>>> df_frame = df.groupby("marker").apply(ret_constant_frame_basic)
>>> df_frame
          val1  val2
marker              
group1 0  1.20  1.30
       1  1.22  1.32
group2 0  1.20  1.30
       1  1.22  1.32

>>> df_single = df.groupby("marker").apply(ret_single_value_from_args, 4.3, 5, args=3, counter={'ct':0})
>>> df_single
marker
group1    4.3
group2    4.3
dtype: float64

>>> df_series = df.groupby("marker").apply(ret_constant_series_from_args, 5.4, 5, arg='arg3')
>>> df_series
        val1  val2
marker            
group1   5.4  arg3
group2   5.4  arg3

>>> df_frame = df.groupby("marker").apply(ret_constant_frame_from_args, 6.1, 'a', arg='arg3')
>>> df_frame
          val1      val2
marker                  
group1 0   6.1      arg3
       1  12.2  arg3arg3
group2 0   6.1      arg3
       1  12.2  arg3arg3

>>> df_agg_single_basic = df.groupby("marker").agg({'value':ret_single_value_basic})
>>> df_agg_single_basic
        value
marker       
group1    1.2
group2    1.2

>>> df_agg_single_nested = df.groupby("marker").agg({'value':[ret_single_value_basic]})
>>> df_agg_single_nested
                        value
       ret_single_value_basic
marker                       
group1                    1.2
group2                    1.2

>>> df_agg_single_all = df.groupby("marker").agg(ret_single_value_from_args, 2.7, args=3)
>>> df_agg_single_all
         id  age  value
marker                 
group1  2.7  2.7    2.7
group2  2.7  2.7    2.7

>>> df_agg_equivalent = df.groupby("marker").apply(ret_agg_value_to_all_columns_from_args, 2.7)
>>> df_agg_equivalent
         id  age  value
marker                 
group1  2.7  2.7    2.7
group2  2.7  2.7    2.7

>>> df_agg_single_basic = df.groupby(["marker", "age"]).agg({'value':ret_single_value_basic})
>>> df_agg_single_basic
             value
marker age        
group1 53.1    1.2
       54.0    1.2
       55.0    1.2
       56.0    1.2
group2 54.0    1.2
       55.0    1.2
       56.0    1.2

>>> df_agg_single_nested = df.groupby(["marker", "age"]).agg({'value':[ret_single_value_basic]})
>>> df_agg_single_nested
                             value
            ret_single_value_basic
marker age                        
group1 53.1                    1.2
       54.0                    1.2
       55.0                    1.2
       56.0                    1.2
group2 54.0                    1.2
       55.0                    1.2
       56.0                    1.2

>>> df_agg_single_all = df.groupby(["marker", "age"]).agg(ret_single_value_from_args, 2.7, args=3)
>>> df_agg_single_all
              id  value
marker age             
group1 53.1  2.7    2.7
       54.0  2.7    2.7
       55.0  2.7    2.7
       56.0  2.7    2.7
group2 54.0  2.7    2.7
       55.0  2.7    2.7
       56.0  2.7    2.7

>>> df_agg_equivalent = df.groupby(["marker", "age"]).apply(ret_agg_value_to_all_columns_from_args, 2.7)
>>> df_agg_equivalent
              id  value
marker age             
group1 53.1  2.7    2.7
       54.0  2.7    2.7
       55.0  2.7    2.7
       56.0  2.7    2.7
group2 54.0  2.7    2.7
       55.0  2.7    2.7
       56.0  2.7    2.7


#docgenend
"""# examples of group by apply
import pandas as pd
import numpy as np

def ret_single_value_basic(dg):
    return 1.2

def ret_constant_series_basic(dg):
    return pd.Series([1.2, 1.3], index=['val1', 'val2'])

def ret_constant_frame_basic(dg):
    return pd.DataFrame.from_dict({'val1': [1.2, 1.22], 
                                   'val2': [1.3, 1.32]})

def ret_agg_value_to_all_columns_basic(dg, *args):
    return pd.Series([1.1] * len(dg.columns), index=list(dg.columns))

def ret_single_value_from_args(dg, *args, **kwargs):
    value1 = args[0]
    value2 = kwargs['args']
    return value1

def ret_constant_series_from_args(dg, *args, **kwargs):
    value1 = args[0]
    value2 = kwargs['arg']
    return pd.Series([value1, value2], index=['val1', 'val2'])

def ret_constant_frame_from_args(dg, *args, **kwargs):
    value1 = args[0]
    value2 = kwargs['arg']
    return pd.DataFrame.from_dict({'val1':[value1, 2 * value1],
                                   'val2':[value2, 2 * value2]})

def ret_agg_value_to_all_columns_from_args(dg, *args):
    value1 = args[0]
    if isinstance(dg.name, str):
        name = [dg.name]
    else:
        name = dg.name
        
    try:
        mask = (dg.isin(name)).values.ravel()
    except:
        import pdb
        pdb.set_trace()
    masked = df.loc[0, mask]
    non_group_columns = list(set(dg.columns) - set(masked.index))
    non_group_columns = dg.columns[np.isin(dg.columns, non_group_columns)]
    return pd.Series([value1] * len(non_group_columns), index=non_group_columns)

df = pd.DataFrame.from_dict({'id':[0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                             'age':[53.1, 54, 56, 54, 55, 56, 54, 55, 56, 54, 55, 55],
                             'marker':['group1', 'group1', 'group1', 'group2', 'group2', 'group2',
                                       'group1', 'group1', 'group1', 'group2', 'group2', 'group2'],
                             'value':[45, 48, 50, 51, 24, -10, 12, 14, 15, -1, -2, -3]})
#markdown
## An example of basic mean  
#* using .function
#* using agg
#* using .apply
#endmarkdown

df_mean = df.groupby("marker").mean()

df_agg_mean = df.groupby("marker").agg('mean')

df_apply_mean = df.groupby("marker").apply(np.mean)

df_single = df.groupby("marker").apply(ret_single_value_basic)

df_series = df.groupby("marker").apply(ret_constant_series_basic)

df_frame = df.groupby("marker").apply(ret_constant_frame_basic)

df_single = df.groupby("marker").apply(ret_single_value_from_args, 4.3, 5, args=3, counter={'ct':0})

df_series = df.groupby("marker").apply(ret_constant_series_from_args, 5.4, 5, arg='arg3')

df_frame = df.groupby("marker").apply(ret_constant_frame_from_args, 6.1, 'a', arg='arg3')


df_agg_single_basic = df.groupby("marker").agg({'value':ret_single_value_basic})

df_agg_single_nested = df.groupby("marker").agg({'value':[ret_single_value_basic]})

df_agg_single_all = df.groupby("marker").agg(ret_single_value_from_args, 2.7, args=3)

df_agg_equivalent = df.groupby("marker").apply(ret_agg_value_to_all_columns_from_args, 2.7)

df_agg_single_basic = df.groupby(["marker", "age"]).agg({'value':ret_single_value_basic})

df_agg_single_nested = df.groupby(["marker", "age"]).agg({'value':[ret_single_value_basic]})

df_agg_single_all = df.groupby(["marker", "age"]).agg(ret_single_value_from_args, 2.7, args=3)

df_agg_equivalent = df.groupby(["marker", "age"]).apply(ret_agg_value_to_all_columns_from_args, 2.7)
#
