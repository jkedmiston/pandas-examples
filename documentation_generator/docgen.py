"""
generate text based documentation from a working standalone script. E.g. you get a printout
of variable definitions and how they change with operations. 

This can be used to generate self maintaining doc strings from example functions, as well as
for general repeated reference. 
"""

import argparse
import pandas as pd
from documentation_generator.file_sniffer import detect_multi_line_assignment
from documentation_generator.file_sniffer import detect_multi_line_function
from documentation_generator.file_sniffer import detect_multi_line_markdown_block
from documentation_generator.file_sniffer import get_text_from_file
from documentation_generator.file_sniffer import write_text_to_file
from documentation_generator.generate_ipynb import generate_ipynb

def write_out_to_jupyter(source, jupyter_str):
    # set up a pre-jupyter document by encolsing blocks in #code/#endcode blocks
    source_jupyter_file = source.replace('.py', '_tmp.py')
    tmp = open(source_jupyter_file, 'w')
    tmp.write(jupyters.replace('\n\n','\n'))
    # code needs to end in # (TODO)
    tmp.write("\n#\n")
    tmp.close()
    #
    generate_ipynb(source=source_jupyter_file, final_output=source.replace('.py', '.ipynb'))

def write_output_at_top_of_file(source, text_to_append_to_top_of_file):
    source_text = get_text_from_file(source, remove_blocks=[['"""#docgenstart', '#docgenend\n"""']])
    source_text = '"""#docgenstart\nFile output (%s): \n%s\n#docgenend\n"""%s' % (source, text_to_append_to_top_of_file, source_text)
    write_text_to_file(source_text, source)
    
def get_text_as_lines(source_text):
    lines = source_text.split("\n")
    lines = list(map(lambda x: x + "\n", lines))
    return lines

if __name__ == "__main__":
    parser = argparse.ArgumentParser('')
    parser.add_argument('source', default="pandas_examples/flattening.py")
    parser.add_argument('--output_file', default='stdout', dest='output_file')
    parser.add_argument('--no_jupyter',
                        default=False,
                        action='store_true',
                        help='dont make the jupyter notebook version')
    
    args = parser.parse_args()
    source = args.source
    output_file = args.output_file
    
    text_to_append_to_top_of_file = ""
    if args.output_file != 'stdout':
        output_file_obj = open(output_file, 'w')
        printfunc = output_file_obj.write
    else:
        printfunc = print

    source_text = get_text_from_file(source,
                                     remove_blocks=[['"""#docgenstart', '#docgenend\n"""']])
    source_lines = get_text_as_lines(source_text)
    
    # execute underlying source to bring in any packages, etc to the current environment. 
    exec(open(source).read())

    file_line_index = 0
    sequence = []
    jupyters = ""
    while file_line_index < len(source_lines):
        l = source_lines[file_line_index]
        file_line_index0 = file_line_index
        sequence.append(file_line_index)

        outval = detect_multi_line_assignment(file_line_index, source_lines)
        outval2 = detect_multi_line_function(file_line_index, source_lines)
        outval3 = detect_multi_line_markdown_block(file_line_index, source_lines)
        
        # TODO: wrap this in function
        # a function was detected
        if outval2["continue"] == 0:
            output = outval2["output"]
            file_line_index = outval2["index"]
            printfunc(output)
            jupyters += "#code\n%s\n#endcode\n" % (output)
            continue

        if outval3["continue"] == 0:
            output = outval3["output"]
            file_line_index = outval3["index"]
            printfunc(output)
            jupyters += "%s\n" % output
            continue
        
        file_line_index = outval["index"] # increment forward
        if outval['continue']:
            if len(l.strip()) > 1:
                jupyters += "#code\n%s\n#endcode\n" % l
                pass
            pass
        else:
            output = outval["output"].strip()
            start, end = output.split("=", 1)
            varname = start.strip()
            end = end.strip()
            if varname.count('.') == 0:
                locals()[varname] = eval(end)
            else:
                # execute the member function e.g. df.apply(), then print out
                exec(output)
                varname = varname.split('.')[0]

            outstr = ">>> %s\n>>> %s\n%s\n" % (output, varname, locals()[varname])
            printfunc(outstr)
            text_to_append_to_top_of_file += outstr + "\n"
            jupyters += "#code\n%s\n%s\n#endcode\n" % (output, varname)
            continue

    # write output at the top of the input file
    write_output_at_top_of_file(source, text_to_append_to_top_of_file)

    
    if args.no_jupyter:
        pass
    else:
        write_out_to_jupyter(args.source, jupyter_str=jupyters)
