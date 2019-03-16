"""
Wrapper to generate ipynb from a py file source. Detects markdown blocks in the source file with
#markdown
#Text
## Heading 1
### Heading 2
#### Heading 3
#* list 1
#* list 2
#endmarkdown
"""
#!/usr/bin/env python
import argparse
import os
from documentation_generator.py_to_ipynb_converter import py_to_ipynb_converter
from documentation_generator.process_ipynb import process_ipynb
from documentation_generator.execute_ipynb import execute_ipynb
import documentation_generator.templates

def generate_ipynb(source, output=None, execute=True, template=documentation_generator.templates.TEMPLATE, final_output=None):
    """
    Default final_output is the source filename.ipynb
    """
    if output is None:
        output = "%s_ipynb_compiler.ipynb" % template[:-6]

    assert template != output, "template must be different than output, as files are overwritten"

    # read from custom markup language to jupyter notebook cells
    py_to_ipynb_converter(template=template, source=source, output=output)

    ipynb_output_file = "%s.ipynb" % source
    if final_output is not None:
        ipynb_output_file = final_output

    # synthesize exec() files in a notebook into a single notebook, reset execution count
    process_ipynb(output, output=ipynb_output_file)

    # run the notebook
    if execute:
        try:
            execute_ipynb(ipynb_output_file)
        except:
            # remove it as the file doesn't work
            # os.system("rm %s" % ipynb_output_file)
            pass
        pass
    pass


if __name__=="__main__":
    parser = argparse.ArgumentParser('''Turns a python file which has the 
    correct custom markup language hooks (see README) into a jupyter notebook with
     .ipynb appended to the original filename''')
    parser.add_argument('source', help="source file (python file). Detects custom markup language, see README. ")
    parser.add_argument('--no_execute', action='store_true', default=False, help="use to prevent execution e.g. if it is a larger notebook")

    parser.add_argument('--output',
                        dest='output',
                        default=None,
                        required=False, help="")
    args = parser.parse_args()


    source = args.source
    generate_ipynb(source=source, output=args.output, execute=not args.no_execute)
