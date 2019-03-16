#!/bin/bash
set -e
export PYTHONPATH=$PYTHONPATH:$IPYNB_REPO
python $GENERATE_IPYNB "$1"
suffix=".py"
fullscript="$1"
py_no_dot_py=${fullscript%"$suffix"}
j=".ipynb"
py_no_dot_py="$py_no_dot_py$j"
pyfull="$(cd "$(dirname "$1")"; pwd -P)/$(basename "$py_no_dot_py")"
pyfull1="$(cd "$(dirname "$1")"; pwd -P)/$(basename "$fullscript").ipynb"
mv $pyfull1 $pyfull
echo $pyfull
if [ "$2" = "run" ]; then
    echo $PYTHONPATH
fi
