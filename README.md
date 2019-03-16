# Pandas examples
* collection of code snippets for dataframe manipulations
* also includes silly file transformations for lazy documentation etc.

# Installation/Environment
* add base directory to PYTHONPATH
```
export PYTHONPATH=/path/to/pandas-examples
```

# First use
```
pytest
```
# Regenerate notebooks
* make_all_notebooks.sh

# Usage
* To generate simple text documentation for a given script. 
```
python documentation_generator/docgen.py pandas_examples/flattening.py 
```
* To generate a jupyter notebook demonstrating plotting scripts. 
```
python documentation_generator/generate_ipynb.py pandas_examples/plotting.py
```
or
```
make
```

# Custom markup language for jupyter notebooks
* use code block structure defined in documentation_generator/examples/basic_notebook.py
* To run example
    - python documentation_generator/generate_ipynb.py documentation_generator/examples/basic_notebook.py 
* Beware multi line files which need to be encoded in the code/endcode blocks, or wrapped in a separate file and then exec(open()) is used to include that file.
* File needs to end in # (TODO)