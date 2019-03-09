# example of grouping plots
# blocks must be contained in either code/endcode blocks or as individual
# executable py files in jupyter_notebook_cells

# TODO: link these into the makefile for the notebook
exec(open("pandas_examples/jupyter_notebook_cells/plotting_import.py").read())

#code
NX = 100
NY = 100
df = pd.DataFrame.from_dict({'id':["id1"] * NX + ["id2"] * NX,
                             'label':['a'] * NX + ['b'] * NX, 
                             'time':list(np.linspace(0, 1, NX)) + list(np.linspace(0, 1, NX)),
                             'dist':list(np.random.normal(loc=.3, size=NX)) + list(np.random.normal(loc=.25, size=NX)),
                             'value':list(np.linspace(1, 2, NX) + np.random.random(NX) * 0.1) + list(np.linspace(1.5, 2.5, NX) + np.random.random(NX) * 0.2)})
df.head()
#endcode
#code
# histogram of "value" for each id
df_group1 = df.groupby("id")[["id", "value"]].get_group("id1")
#endcode

#markdown
#Here we show some results
#endmarkdown
#code
grped = df.groupby("id")
fig, ax = plt.subplots(1, 1)
for g in grped.groups.keys():
    dg = grped.get_group(g)
    ax.hist(dg["dist"], bins=20, histtype='step', stacked=False, label=g)
    pass
ax.legend()
fig.show()
#endcode
#markdown
# can  this be produced in one line?
#endmarkdown
#code
fig, ax = plt.subplots(1, 1)
df.groupby("id")[["id", "dist"]].plot(kind="hist", ax=ax, label="id", by="id")
ax.legend()
fig.show()
#endcode
#markdown 
#reference [ref](https://stackoverflow.com/questions/29975835/how-to-create-pandas-groupby-plot-with-subplots)
#endmarkdown


#markdown
#some results
#endmarkdown
#code
df["idd"] = df.index
out = pd.pivot_table(df.reset_index(), index="idd", values="dist", columns="id").plot(subplots=True, kind='hist', histtype='step', stacked=True)
out[0].figure.show()
#endcode
#code
out = pd.pivot_table(df.reset_index(), index="index", values="dist", columns="id")
out.head()
#endcode
#markdown
#more results
#hello
#* hello
#endmarkdown
#code
out = pd.pivot_table(df.reset_index(), index="index", values="dist", columns="id").plot(subplots=True, kind='hist', histtype='step', stacked=True)
out[0].figure.show()
#endcode

#code
rowlength = int(grped.ngroups/2)                         # fix up if odd number of groups
fig, axs = plt.subplots(figsize=(9,4), 
                        nrows=2, ncols=rowlength,     # fix as above
                        gridspec_kw=dict(hspace=0.4)) # Much control of gridspec

targets = zip(grped.groups.keys(), axs.flatten())
for i, (key, ax) in enumerate(targets):
    ax.hist(grped.get_group(key)["dist"])
    ax.set_title('a=%s'%key)
    pass
#endcode
#
