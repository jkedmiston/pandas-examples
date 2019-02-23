"""
These tests simply exercise code and do not analyze the results
"""
import os
import documentation_generator.templates
from documentation_generator.py_to_ipynb_converter import py_to_ipynb_converter
from documentation_generator.process_ipynb import process_ipynb
from documentation_generator.execute_ipynb import execute_ipynb

def test_examples_stated_in_readme():
    """test the examples in the README
    #TODO: set up this to automatically parse the README
    """
    template = documentation_generator.templates.TEMPLATE

    tmp = 'tests/tmp_readme.ipynb'
    py_to_ipynb_converter(template=template, source='pandas_examples/plotting.py', output=tmp)

    # synthesize exec lines, reset count
    ipynb_output_file = "tests/out_readme.ipynb"
    process_ipynb(tmp, output=ipynb_output_file)

    # execute nb
    print(os.path.abspath(ipynb_output_file))
    execute_ipynb(ipynb_output_file)
    os.system("rm %s %s" % (tmp, ipynb_output_file))
    
def test_notebook_creation():
    """test the example in documenation generator"""
    template = documentation_generator.templates.TEMPLATE

    tmp = 'tests/tmp_notebook.ipynb'
    py_to_ipynb_converter(template=template, source='documentation_generator/examples/basic_notebook.py', output=tmp)

    # synthesize exec lines, reset count
    ipynb_output_file = "documentation_generator/examples/basic_notebook.ipynb"
    process_ipynb(tmp, output=ipynb_output_file)

    # execute nb
    print(os.path.abspath(ipynb_output_file))
    execute_ipynb(ipynb_output_file)

    os.system("rm %s %s" % (tmp, ipynb_output_file))
    
if __name__=="__main__":
    test_notebook_creation()
    test_examples_stated_in_readme()
