"""
generate text based documentation from a working standalone script
"""
import argparse
import pandas as pd
from documentation_generator.file_sniffer import detect_multi_line_assignment

parser = argparse.ArgumentParser('')
parser.add_argument('source', default="pandas_examples/flattening.py")
parser.add_argument('--output_file', default='stdout', dest='output_file')
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
while index < len(lines):
    l = lines[index]
    index0 = index
    sequence.append(index)
    outval = detect_multi_line_assignment(index, lines)
    index = outval["index"]
    if outval['continue']:
        continue

    output = outval["output"].strip()
    start, end = output.split("=", 1)
    varname = start.strip()
    end = end.strip()
    if varname.count('.') == 0:
        locals()[varname] = eval(end)
    else:
        exec(output)
        varname = varname.split('.')[0]

    outstr = ">>> %s\n>>> %s\n%s\n" % (output, varname, locals()[varname])
    printfunc(outstr)#output_file_obj.write(outstr)
    continue
