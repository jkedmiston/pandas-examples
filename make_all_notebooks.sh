#!/bin/bash
set -e
export PYTHONPATH=$PWD:$PYTHONPATH
python documentation_generator/docgen.py pandas_examples/flattening.py
python documentation_generator/docgen.py pandas_examples/applying.py 
python documentation_generator/generate_ipynb.py pandas_examples/plotting.py
