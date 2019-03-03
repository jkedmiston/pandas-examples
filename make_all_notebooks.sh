#!/bin/bash
set -e
export PYTHONPATH=$PWD:$PYTHONPATH

# produces pandas_examples/flattening.ipynb
python documentation_generator/docgen.py pandas_examples/flattening.py

# produces pandas_examples/applying.ipynb
python documentation_generator/docgen.py pandas_examples/applying.py

# produces pandas_examples/plotting.py.ipynb
python documentation_generator/generate_ipynb.py pandas_examples/plotting.py

# produces documentation_generator/examples/basic_notebook.ipynb
./generate_nb.sh documentation_generator/examples/basic_notebook.py
