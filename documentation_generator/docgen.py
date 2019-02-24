"""
generate text based documentation from a working standalone script
Useful for generating doc strings which update from a working python script. 
"""
import argparse
import pandas as pd
from documentation_generator.file_sniffer import detect_multi_line_assignment
from documentation_generator.generate_ipynb import generate_ipynb

if __name__ == "__main__":
    parser = argparse.ArgumentParser('')
    parser.add_argument('source', default="pandas_examples/flattening.py")
    parser.add_argument('--output_file', default='stdout', dest='output_file')
    parser.add_argument('--jupyter', default=None, action='store_true')
    args = parser.parse_args()

    source = args.source
    output_file = args.output_file
    if args.output_file != 'stdout':
        output_file_obj = open(output_file, 'w')
        printfunc = output_file_obj.write
    else:
        printfunc = print

    f = open(source, 'r')
    lines = f.readlines()
    f.close()

    # execute underlying source to bring in any packages, etc. 
    exec(open(source).read())

    index = 0
    sequence = []
    jupyters = ""
    while index < len(lines):
        l = lines[index]
        index0 = index
        sequence.append(index)
        outval = detect_multi_line_assignment(index, lines)
        index = outval["index"] # increment forward
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
            jupyters += "#code\n%s\n%s\n#endcode\n" % (output, varname)
            continue
    source_jupyter_file = args.source.replace('.py', '_tmp.py')
    tmp = open(source_jupyter_file, 'w')
    tmp.write(jupyters.replace('\n\n','\n'))
    tmp.write("\n#\n")
    tmp.close()
    #
    generate_ipynb(source=source_jupyter_file, final_output=args.source.replace('.py', '.ipynb'))
